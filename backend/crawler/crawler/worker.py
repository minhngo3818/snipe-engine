from threading import Thread

from inspect import getsource
from utils.download import download
from utils import get_logger, get_urlhash, get_main_url
from utils.trap_cache import trap_cache
import scraper
import time


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break
            
            # Check if url is in pattern list
            main_url = get_main_url(tbd_url)
            hash_url = get_urlhash(main_url)

            if trap_cache.is_trap_url(hash_url):
                # Skip the page if it is in the trap cache
                self.logger.info(
                    f"Infinite trap or poor content! -- Skip {tbd_url}, " 
                    f"using cache {self.config.cache_server}.")
            else:
                resp = download(tbd_url, self.config, self.logger)
                self.logger.info(
                    f"Downloaded {tbd_url}, status <{resp.status}>, "
                    f"using cache {self.config.cache_server}.")
                scraped_urls = scraper.scraper(tbd_url, resp, self.config)
                for scraped_url in scraped_urls:
                    self.frontier.add_url(scraped_url)

            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
