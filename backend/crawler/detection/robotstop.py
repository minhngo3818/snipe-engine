from urllib.parse import urlparse, urljoin
from utils import get_urlhash


"""
    @summary: Check disallowed paths defined in robots.txt
    under a domain
"""
class RobotStop:
    def __init__(self):
        # { key: netloc, value: {visited: , path: []} }
        self.robot_urls = {} 

        
    def is_robot_txt(self, path):
        return "robots.txt" in path


    def is_disallowed(self, netloc, path):
        hash_netloc = get_urlhash(netloc)
        if not self.robot_urls.get(hash_netloc):
            return False

        return path in self.robot_urls[hash_netloc]["paths"]


    def get_robots_url(self, base_url):
        # Get url contain robots.txt
        # Must be called intially before crawling any subsequence pages

        parsed = urlparse(base_url)
        hash_netloc = get_urlhash(parsed.netloc)
        if parsed.netloc in self.robot_urls:
            if not self.robot_urls[hash_netloc]:
                self.robot_urls[hash_netloc]["visited"] = True
            return None

        self.robot_urls[hash_netloc] = {"visited": False, "paths": []}

        return urljoin(parsed.scheme, parsed.netloc, "robots.txt")


    def append_disallowed_path(self, url, response_content):
        # Break down robots.txt file and acquire disallowed paths
        # specified under User-agent * (bot)

        parsed = urlparse(url)
        user_agent = "*"
        hash_netloc = get_urlhash(parsed.netloc)
        user_agent_lines = []  
        for line in response_content.splitlines():
            if line.startswith("User-agent:") and user_agent in line:
                user_agent_lines.append()

        for line in user_agent_lines:
            if "Disallow:" in line:
                disallowed_path = line.split("Disallow:")[1].strip()
                
                if self.robot_urls.get(hash_netloc):
                    self.robot_urls[hash_netloc]["paths"].append(disallowed_path)


robotstop = RobotStop()
