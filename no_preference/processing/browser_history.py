import os
import re
from datetime import datetime
from typing import List, Dict, Union
from urllib.parse import urlparse

import pandas as pd
import requests
import requests_cache
from bs4 import BeautifulSoup
from dateutil.parser import parse
from pandas import DataFrame
from spacy.tokens.doc import Doc
from spacy.tokens.token import Token

from no_preference.util import get_logger


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

LOGGER = get_logger(__name__)

requests_cache.install_cache()


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
        LOGGER.warning(f'Could not load URL "{url}".')
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


def _load_history_text(urls: List[str]) -> List[str]:
    relevant_urls = _filter_urls(urls)
    relevant_urls_len = len(relevant_urls)
    LOGGER.info('Loading {} relevant URLs out of {} history entries.'.format(relevant_urls_len, len(urls)))
    history_text = []
    for i, url in enumerate(relevant_urls):
        LOGGER.info(f'{i}/{relevant_urls_len}: Loading "{url}".')
        url_text = _get_url_text(url)
        if url_text:
            history_text.append(url_text)
    return history_text


def load_history(history: DataFrame, from_time: datetime = None, to_time: datetime = None) -> DataFrame:
    # Filter by visit time
    if from_time or to_time:
        if not from_time:
            from_time = datetime.fromtimestamp(0)
        if not to_time:
            to_time = datetime.now()

        history = history[(from_time <= history['last_visit_time']) & (history['last_visit_time'] <= to_time)]

    return DataFrame(zip(history['last_visit_time'], _load_history_text(history['url'])),
                     columns=['last_visit_time', 'text'])


if __name__ == '__main__':
    csv = pd.read_csv('../../datasets/chrome_history_nathan.csv', parse_dates=['last_visit_time'], date_parser=parse)
    results = load_history(csv, from_time=datetime(2019, 10, 23), to_time=datetime(2019, 10, 23, 23, 59, 59))
    print(results)
