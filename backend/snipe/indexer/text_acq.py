from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
from urllib.parse import urlparse
import warnings
import os
import json


def get_page_list(dataset_dir):
    """
    Get a list of file path from dataset

    Parameters:
    - dataset_dir (str): directory to dataset

    Return:
    - a stream of file paths
    """

    for root, dirs, files in os.walk(dataset_dir):
        for f in files:
            yield (os.path.join(root, f))


def extract_page_content(content):
    """
    Extract 'content' in json data
    Categorize content into groups: title, header, strong, and text
    This helps indexing process

    Parameter:
    - content (str): textual content of a page from json file

    Return:
    - A dictionary with each key corresponding to each group
    and value type string (for the purpose of text transformation process)

    """
    warnings.simplefilter("error", MarkupResemblesLocatorWarning)
    try:
        soup_parser = BeautifulSoup(content, "lxml-xml")

        # Acquire text from <title>
        title_tags = soup_parser.find_all("title")
        title = (
            " ".join([title.text for title in title_tags]).replace("\n", " ").strip()
        )

        # Get text from h tag
        header_tags = soup_parser.find_all(
            lambda tag: tag.name
            and tag.name.lower() in {"h1", "h2", "h3", "h4", "h5", "h6"}
        )
        header = (
            " ".join([header.text for header in header_tags]).replace("\n", " ").strip()
        )

        # Get text from strong tag
        strong_tags = soup_parser.find_all("strong")
        strong = (
            " ".join([strong.text for strong in strong_tags]).replace("\n", " ").strip()
        )

        # Remove parsed tags
        for tag in title_tags + header_tags + strong_tags:
            tag.decompose()

        # Get text from the other tags
        text = soup_parser.get_text().replace("\n", "").strip()

        return {"title": title, "header": header, "strong": strong, "text": text}

    except MarkupResemblesLocatorWarning as e:
        print(e)
        return None


def read_page(file_path):
    """
    Read data file and extract page name, url, and content

    Parameters:
    - file_path (str) path to data file

    Return:
    - None if there is not content or error
    - A dictionary contains page_title, url, and content dictionary
    """
    data_file = open(file_path, "r")
    data = json.load(data_file)
    data_file.close()
    url = data.get("url")
    content_dict = extract_page_content(data.get("content"))

    if not content_dict:
        return None
    else:
        title = content_dict.get("title")
        page_title = urlparse(url).hostname if len(title) == 0 else title
        return {"page_title": page_title, "url": url, "content_dict": content_dict}
