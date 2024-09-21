import re
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from report_tasks import report_tasks
from detection.robotstop import robotstop
from detection.looptrap import is_depth_trap, simhash_url
from utils import get_urlhash, normalize_sub_url, get_main_url
from utils.trap_cache import trap_cache
from detection.redirect import redirect_resp


def scraper(url, resp, config):
    if resp.status < 200 or resp.status >= 400:
        print("ERROR: {} {} - Skip page".format(resp.status, resp.error))
        return list()

    actual_response = resp
    actual_url = url

    if resp.status in range(300, 400):
        print("INFO: Found redirect response")
        response_3xx = redirect_resp(actual_response, config)

        if response_3xx:
            actual_response = response_3xx
            actual_url = response_3xx.url

    if resp.status == 200 and not resp.raw_response.content:
        print("ERROR: Page has no content")
        return list()
            
    links = extract_next_links(actual_url, actual_response)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    # Check paths in robots.txt under a domain
    if robotstop.is_robot_txt(url):
        robotstop.append_disallowed_path(url, resp.raw_response.content)

    hyperlinks = []
    robot_txt_url = robotstop.get_robots_url(url)

    if robot_txt_url:
        hyperlinks.append(robot_txt_url)

    soup_page = BeautifulSoup(resp.raw_response.content, 'lxml')
    
    # Page is duplicated or trap if read_page return true
    # Force to yield empty url to prevent further trap reading
    if report_tasks.read_page(soup_page.text, url):
        return hyperlinks

    for link in soup_page.find_all("a"):
        sub_link = link.get("href")

        # Prevent adding page with # in href
        if sub_link != "#":
            normalized_url = normalize_sub_url(sub_link, resp.url)
            hyperlinks.append(normalized_url)

    return hyperlinks


def is_valid(url):

    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)

        if parsed.scheme not in set(["http", "https"]):
            return False

        if (".ics.uci.edu" not in parsed.netloc
            and ".cs.uci.edu" not in parsed.netloc
            and ".informatics.uci.edu" not in parsed.netloc
            and ".stat.uci.edu" not in parsed.netloc):
            return False

        # Prevent access banned paths from bot
        if robotstop.is_disallowed(parsed.netloc, parsed.path):
            return False

        # Check false path that has multiple same path fragment or too long path
        if is_depth_trap(parsed.path, len(url)):
            return False

        # Simhash url and check if its finger print already existed
        if simhash_url.simhash_check_exist(parsed):
            # Get the main path that has only domain and paths
            pattern_url = get_main_url(url)
            hash_pattern_url = get_urlhash(pattern_url)

            if trap_cache.is_trap_url(hash_pattern_url) is None:
                # Add discovered trap url to trap cache
                trap_cache.set_trap_url(hash_pattern_url, False)
            elif trap_cache.is_trap_url(hash_pattern_url):
                # Return false immediately if trap path is verified
                return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
