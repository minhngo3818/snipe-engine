import os
import logging
from hashlib import sha256
from urllib.parse import urlparse, urlunparse, parse_qs


def get_logger(name, filename=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not os.path.exists("Logs"):
        os.makedirs("Logs")
    fh = logging.FileHandler(f"Logs/{filename if filename else name}.log")
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def get_urlhash(url):
    parsed = urlparse(url)
    # everything other than scheme.
    return sha256(
        f"{parsed.netloc}/{parsed.path}/{parsed.params}/"
        f"{parsed.query}/{parsed.fragment}".encode("utf-8")).hexdigest()


def normalize(url):
    if url.endswith("/"):
        return url.rstrip("/")
    return url


def normalize_sub_url(sub_url: str, base_url: str) -> str:
    # Convert non absolute urls acquired from parsing page

    parsed_url = urlparse(sub_url)

    if not parsed_url.scheme or not parsed_url.netloc:
        parsed_base_url = urlparse(base_url)
        scheme = parsed_base_url.scheme
        domain = parsed_base_url.netloc
        path = parsed_url.path or ""
        params = parsed_url.params or ""
        query = parsed_url.query or ''
        fragment = parsed_url.fragment or ""
        # Reconstruct url
        completed_url = urlunparse((scheme, domain, path,
                                    params, query, fragment))
        return completed_url
    else:
        return sub_url


def get_main_url(url: str) -> str:
    # Get url containing scheme, netloc, and path only

    parsed_url = urlparse(url)
    return urlunparse((parsed_url.scheme, parsed_url.netloc,
                       parsed_url.path, "", "", ""))


def get_url_component_list(parsed_url):
    # Breakdown tokens of url base on url components
    # Helper for simhash url
    component_list = [
        parsed_url.scheme,
        parsed_url.netloc,
    ]

    # Break down path tokens
    path_elements = parsed_url.path.split("/")
    path_elements = [element.split("-") for element in path_elements]
    flattened_elements = [item for sublist in path_elements for item in sublist]
    component_list.extend(flattened_elements)

    # Break down params value
    params_dict = parse_qs(parsed_url.query)
    for param, values in params_dict.items():
        component_list.extend(values)

    # Add the rest components
    component_list.extend(parsed_url.params)
    component_list.extend(parsed_url.fragment)

    return component_list
