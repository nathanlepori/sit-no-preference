import re
import warnings
import pandas as pd
import requests
import requests_cache
import logging

from typing import Iterator, List, Pattern
from urllib.error import URLError
from bs4 import BeautifulSoup

IRRELEVANT_URL_PATTERNS = [
    # Search engines queries
    r'^https://www\.google\.com/search.*$',
    r'^https://www\.bing\.com/search.*$',
    # Supported social media
    r'^https://twitter\.com/.*$',
    r'^https://www\.facebook\.com/.*$'
]

logging.root.setLevel(logging.INFO)

requests_cache.install_cache()


def _flatten(l: List[List]) -> List:
    return [item for sublist in l for item in sublist]


def _get_url_text(url: str) -> List[str]:
    # Read URL and create DOM object
    response = requests.get(url)
    html = response.text
    dom = BeautifulSoup(html)

    # Remove all code tags
    for code in dom(['script', 'style']):
        code.extract()

    text: str = dom.get_text()
    return text.splitlines()


def _clean_url_text(url_text: List[str]) -> List[str]:
    # Remove empty lines
    url_text = filter(lambda line: not re.match(r'^\s*$', line), url_text)
    # Remove leading and trailing whitespaces
    url_text = map(lambda line: line.strip(), url_text)

    return list(url_text)


def _tokenize_url_text(url_text: List[str]) -> List[str]:
    # Extract tokens by multiple separators
    tokens = list(map(lambda line: re.split(r'\s|\. |: |, ', line), url_text))

    # Flatten and return list
    return _flatten(tokens)


def _get_url_tokens(url: str) -> List[str]:
    text = _get_url_text(url)
    if not text:
        return []
    text = _clean_url_text(text)
    tokens = _tokenize_url_text(text)
    return tokens


def is_irrelevant_url(url: str) -> bool:
    for pattern in IRRELEVANT_URL_PATTERNS:
        if re.match(pattern, url):
            return True
    return False


def _filter_urls(urls: List[str]) -> List[str]:
    """
    Removes duplicate entries, irrelevant URLs (like search engine queries), ...
    :param urls:
    :return:
    """
    # Remove duplicates
    urls = set(urls)

    # Filter irrelevant URLs
    return list(filter(lambda url: not is_irrelevant_url(url), urls))


def get_history_tokens(urls: List[str]):
    urls_len = len(urls)
    urls = _filter_urls(urls)
    relevant_urls_len = len(urls)
    logging.info('Analysing {} relevant URLs out of {} history entries.'.format(relevant_urls_len, urls_len))
    tokens = []
    for url in urls:
        logging.info('Loading {}'.format(url))
        tokens.append(_get_url_tokens(url))
    return tokens


if __name__ == '__main__':
    csv = pd.read_csv('../../datasets/chrome_history.csv')
    urls = csv['URL']
    tokens = get_history_tokens(urls)
    print(tokens)
