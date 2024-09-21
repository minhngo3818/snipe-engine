import re
from detection.simidup import simidup_ngram
from utils import get_main_url, get_urlhash
from utils.trap_cache import trap_cache
from urllib.parse import urlparse, urlunparse
import json
import os


"""
    @summary: 
    Process the content of visited page
    Record all data for question 1 to 4 during crawling process
"""
class ReportTasks:
    def __init__(self):
        self.stop_words = []
        self.stopwords_path = "english_stopwords.txt"
        with open(self.stopwords_path, 'r', encoding='utf-8') as file:
            self.stop_words = file.read().splitlines()

        self.report_file = os.path.join("data", "report_data.json")
        if os.path.exists(self.report_file):
            os.remove(self.report_file)

        self.is_load_success = False
        try:
            with open(self.report_file, "r") as report_data:
                self.loaded_data = json.load(report_data)
                self.is_load_success = True
        except:
            self.loaded_data = {
                "t1_unique": {},
                "t2_max_token": {"url": "", "count": 0},
                "t3_all_freq": {},
                "t4_subdomains": {}
            }

    def tokenize(self, page_content):
        # Get a list of tokens from page content called from an url
        # Process and remove stopword

        alphanumeric = re.compile(r'[a-zA-Z0-9]+', re.IGNORECASE)
        raw_tokens = re.findall(alphanumeric, page_content)
        final_tokens = []

        for token in raw_tokens:
            if token.lower() not in self.stop_words:
                final_tokens.append(token.lower())

        return final_tokens

    def top_50_common_words(self, tokens):
        top_fifty = []
        count = 0

        for token in tokens:
            if count == 50:
                break

            if token not in self.stop_words:
                top_fifty.append(token)
                count += 1

        return top_fifty

    def count_unique_pages(self, url):
        # Question 1: record unique pages
        base = url.split("#")[0]
        if base in self.loaded_data["t1_unique"]:
            self.loaded_data["t1_unique"][base] += 1
        else:
            self.loaded_data["t1_unique"][base] = 1

        self.save()

    def update_max_token(self, token_list, url):
        # Question 2: find the url which is the longest page based on number of tokens
        if len(token_list) > self.loaded_data["t2_max_token"].get("count", 0):
            self.loaded_data["t2_max_token"]["url"] = url
            self.loaded_data["t2_max_token"]["count"] = len(token_list)
            self.save()

    def get_token_frequencies(self, token_list):
        # Question 3: get frequencies of all tokens throughout the process
        
        # Get the frequencies of filtered token
        word_frequencies = {}

        for token in token_list:
            if token in word_frequencies:
                word_frequencies[token] += 1
            else:
                word_frequencies[token] = 1

        # sort frequencies
        word_frequencies = dict(sorted(word_frequencies.items(),
                                       key=lambda item: (-item[1], item[0])))

        for token, freq in word_frequencies.items():
            if token in self.loaded_data["t3_all_freq"]:
                self.loaded_data["t3_all_freq"][token] += freq
            else:
                self.loaded_data["t3_all_freq"][token] = freq

        self.save()

    def count_subdomains(self, url):
        # Question 4: count subdomain under a domain
        
        base = urlparse(url)
        check = urlunparse((base.scheme, base.hostname, '', '', '', ''))
        if(check in self.loaded_data["t4_subdomains"]):
            self.loaded_data["t4_subdomains"][check] += 1
        else:
            self.loaded_data["t4_subdomains"][check] = 1
            keys_sorted = sorted(self.loaded_data["t4_subdomains"].keys())
            updated_dict = {i: dict[i] for i in keys_sorted}
            self.loaded_data["t4_subdomains"].clear()
            self.loaded_data["t4_subdomains"] = updated_dict

        self.save()

    def save(self):
        with open(self.report_file, 'w') as json_file:
            json.dump(self.loaded_data, json_file)

    def read_page(self, content, url):
        # Reads the input url page and report in CRAWLER.log
        # update max tokens along with url

        token_list = self.tokenize(content)
        is_simidup = simidup_ngram.ngram_compare(token_list)
        self.get_token_frequencies(token_list)
        self.update_max_token(token_list, url)
        self.count_unique_pages(url)
        self.count_subdomains(url)

        # Check nearest similar or duplicated page, verify if it is
        if is_simidup:
            main_url = get_main_url(url)
            hash_url = get_urlhash(main_url)

            if not trap_cache.is_trap_url(hash_url):
                trap_cache.set_trap_url(hash_url, True)

            return True

        return False


report_tasks = ReportTasks()
