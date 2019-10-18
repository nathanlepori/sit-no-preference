import logging
import os
import random
import re
import pandas as pd
import requests
import requests_cache

from bs4 import BeautifulSoup
from spacy.lang.en import English
from spacy.tokens.doc import Doc
from spacy.tokens.token import Token
from typing import List, Dict, Union
from urllib.parse import urlparse

from src.processing.util import filter_tokens, get_tokens_count


class HistoryAnalysisResults:
    doc: Doc
    relevant_tokens: List[Token]
    relevant_tokens_count: Dict[Token, int]


WEB_CONTENT_EXTENSIONS_PATTERN = r'(\.(aspx?|x?html?|php(3|4)|jspx?))?'
IRRELEVANT_URL_PATTERNS = [
    # Search engines homepages and queries
    r'^https?:\/\/(www\.)?google\.com\/?\??.*$',
    r'^https?:\/\/(www\.)?google\.com\/search.*$',
    r'^https?:\/\/(www\.)?bing\.com\/?\??.*$',
    r'^https?:\/\/(www\.)?bing\.com\/search.*$',
    # Supported social media (analysed separately)
    r'^https?:\/\/(www\.)?twitter\.com.*$',
    r'^https?:\/\/(www\.)?facebook\.com.*$',
]

PUNCTUATION = '. ? ! , ; : - _ – [ ] { } ( ) < > \' " ... # ° § \n & “ ” @ / \\'.split()

logging.root.setLevel(logging.INFO)

requests_cache.install_cache()


def _flatten(l: List[List]) -> List:
    return [item for sublist in l for item in sublist]


def _get_url_extension(url: str) -> str:
    path = urlparse(url).path
    return os.path.splitext(path)[1]


def _is_relevant_url(url: str) -> bool:
    for pattern in IRRELEVANT_URL_PATTERNS:
        if re.match(pattern, url):
            return False

    url_ext = _get_url_extension(url)
    return bool(re.match(WEB_CONTENT_EXTENSIONS_PATTERN, url_ext))


def _filter_urls(urls: List[str]) -> List[str]:
    """
    Removes duplicate entries, irrelevant URLs (like search engine queries), ...
    :param urls:
    :return:
    """
    # Remove duplicates
    urls = set(urls)

    # Filter irrelevant URLs
    return list(filter(_is_relevant_url, urls))


def _get_url_text(url: str) -> Union[str, None]:
    # Read URL and create DOM object
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        logging.warning(f'Could not load URL "{url}".')
        return
    html = response.text
    dom = BeautifulSoup(html, 'html.parser')

    # Remove all code tags
    for code in dom(['script', 'style']):
        code.extract()

    text: str = dom.get_text(separator=' ')

    # Remove empty line, trim each line and reassemble the string
    filtered_text = '\n'.join(
        map(lambda line: line.strip(),
            filter(lambda line: not re.match(r'^\s*$', line), text.splitlines())))

    return filtered_text


def _load_history_text(urls: List[str]):
    relevant_urls = _filter_urls(urls)
    logging.info('Loading {} relevant URLs out of {} history entries.'.format(len(relevant_urls), len(urls)))
    history_text = ''
    for url in relevant_urls:
        logging.info('Loading "{}".'.format(url))
        url_text = _get_url_text(url)
        if url_text:
            history_text += ' ' + url_text
    return history_text


def _remove_history_stop_words(history_doc: Doc):
    pass


def _analyse_history_text(history_text: str) -> HistoryAnalysisResults:
    nlp = English()

    results = HistoryAnalysisResults()
    results.doc = nlp(history_text)
    results.relevant_tokens = filter_tokens(results.doc)
    results.relevant_tokens_count = get_tokens_count(results.relevant_tokens)

    return results


def analyse_history(urls: List[str], samples=None) -> HistoryAnalysisResults:
    if samples:
        urls = random.choices(urls, k=samples)

    history_text = _load_history_text(urls)
    return _analyse_history_text(history_text)


if __name__ == '__main__':
    csv = pd.read_csv('../../datasets/chrome_history.csv')
    results = analyse_history(csv['url'], 500)
