Web Crawler 

  
Install Dependencies
- Require: Python (>= 3.6)
  - You can download and install Python from [python.org](https://www.python.org/downloads/).

- To install (python3 if using linux)
  ```
  python -m pip install packages/spacetime-2.1.1-py3-none-any.whl
	python -m pip install -r packages/requirements.txt
  ```

- Optional: require gcc
  ```
  make install
  ```

Usage 
- To execute the crawler run the launch.py command:
  ```
  python3 launch.py
  ```
- Can restart the crawler from the seed url (all current progress will be deleted) using the command:
  ```
  python3 launch.py --restart
  ```
- Can specify a different config file to use by using the command with the option:
  ```
  python3 launch.py --config_file path/to/config
  ```

Files
- scraper.py
  * scraper(url, resp): takes the url that was added to the frontier/downloaded from the cache and the resp given by the caching server for the requested url which returns a list of urls that are scraped from the response. 
  * extract_next_links(url, resp): takes the url and resp which returns a list with the hyperlinks, as strings, from the resp.raw_response.content. 
  * is_valid(url, url_prev): takes the url to decide whether or not to crawl, which returns a boolean. 

- report_tasks.py
  * Class ReportTasks
    - tokenize(self, page_content): takes the page_content and tokenizes its characters, which returns a list of all the tokens within that page. 
    - top_50_common_words(self, tokens): takes the list of all the tokens from the pages and returns the top 50 words. 
    - count_unique_pages(self, url): takes a URL, removes the fragment, the url gets added to a dictionary, and if the key already exists,         the value (representing the frequency) is incremented. All keys with a value of 1 are considered unique.
    - update_max_token(self, token_list, url): updates/saves the longest list of tokens.
    - get_token_frequencies(self, token_list): takes the list of tokens from the pages and returns a sorted word frequncy dictionary. 
    - count_subdomains(self, url): takes a URL, keeps the scheme+base, adds it to a dictionary if it doesn't already exist and increment           the value which corresponds to the number of unique pages that the url contains.
    - save(self): dumps/writes all the currently saved data into the json. 
    - read_page(self, content, url): reads the url given in the function and tokenizes all the content on the page. Dictionaries for counting unique URLs, subdomains, and update_max_token are all called in this function. Verify page if page is similar or duplicates to trap cache

- detection/looptrap.py
  * is_depth_trap(): check repeated path /abc/abc/abc or too long url
  * Class SimhashUrl: simhash url to prevent infite trap
    - simhash_prehash_sha256_bin(token, hash_size): hash url into sha256, encode base on hash size, then convert to binary string
    - simhash(parsed_url, hash_size): create a finger print from prehashed token (from url), then simhash it into binary number string, store in avl tree
    - simhash_check_exist(parsed_url, hash_size=64): find the closest node in tree and calculate hamming distance, return true if it is greater than 0.9 tolerant
    - save(): save hash into avl tree in a pickle file

- detection/redirect.py:
  * redirect_resp(resp, config): excavate direct urls until it reach 200 status page, exit when it is too deep to dig. Still ensure politeness

- detection/robotstop:
  * Class RobotStop: check the domain robots.txt to not access certain path
    - is_robot_txt(path): return true if domain has robots.txt
    - is_disallowed(netloc, path): return true if url is not allowed
    - get_robots_url(base_url): construct url contains robots.txt
    - append_disallowed_path(url, response_content): process content of robots.txt and add non-allowed paths

- detection/simidup.py:
  * Class SuimidupNgram: check nearly similar page using 3-gram algorithm
    - ngram_to_crc_number(ngram): encode ngram string crc number base 32
    - ngram_fg(tokens, n=3): convert entire page into a list of 3-gram string, calculate crc number for each 3-gram string, return finger print by mod 4 selection
    - ngram_similarity(tokens): calculate ratio of intersection/union of two set, return true if the ratio is greater than 0.9 tolereant
    - ngram_compare(tokens): find the nearest node in avl tree and check similarity between two set, store finger print in pickle file in avl tree, return true if they are similar
    - save(): store data in pickle file

- utils/trap_cache.py:
  * Class TrapUrlCache: store infinite trap url in a time-to-live cache, remove url if it live longer than 15min
    - set_trap_url(key, value): set sha256 hash url in the cache with isTrap(boolean) and timestamp, store data in a pickle file
    - is_trap_url(key): check if the key is True which indicates a trap.

- crawler/woker.py modify run() that if url in the trap cache, then skip and mark visited, otherwise, process scraper as usual