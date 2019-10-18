import re
import warnings
from collections import OrderedDict

import pandas as pd
import requests
import requests_cache
import logging

from typing import Iterator, List, Pattern, Iterable, Dict, Tuple, Union
from urllib.error import URLError
from bs4 import BeautifulSoup
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
from spacy.tokens.doc import Doc
from spacy.tokens.token import Token


class HistoryAnalysisResults:
    doc: Doc
    relevant_tokens: List[Token]
    relevant_tokens_count: Dict[Token, int]


IRRELEVANT_URL_PATTERNS = [
    # Search engines homepages and queries
    r'^https?:\/\/(www\.)?google\.com\/?\??.*$',
    r'^https?:\/\/(www\.)?google\.com\/search.*$',
    r'^https?:\/\/(www\.)?bing\.com\/?\??.*$',
    r'^https?:\/\/(www\.)?bing\.com\/search.*$',
    # Supported social media
    r'^https?:\/\/(www\.)?twitter\.com.*$',
    r'^https?:\/\/(www\.)?facebook\.com.*$',
]

PUNCTUATION = '. ? ! , ; : - _ – [ ] { } ( ) < > \' " ... # ° § \n & “ ” @ / \\'.split()

logging.root.setLevel(logging.INFO)

requests_cache.install_cache()


def _flatten(l: List[List]) -> List:
    return [item for sublist in l for item in sublist]


def _is_relevant_url(url: str) -> bool:
    for pattern in IRRELEVANT_URL_PATTERNS:
        if re.match(pattern, url):
            return False
    return True


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


def _is_relevant_token(token: Token) -> bool:
    """
    Returns whether the token is relevant, aka not a stop-word, not punctuation, not newline, and not empty or
    whitespace.
    :param token:
    :return:
    """
    return not token.is_stop and len(token.text.strip()) != 0 and token.text not in PUNCTUATION


def _filter_tokens(doc: Doc):
    return list(filter(_is_relevant_token, doc))


def _analyse_history_text(history_text: str) -> HistoryAnalysisResults:
    nlp = English()

    results = HistoryAnalysisResults()
    results.doc = nlp(history_text)
    results.relevant_tokens = _filter_tokens(results.doc)
    results.relevant_tokens_count = get_tokens_count(results.relevant_tokens)

    return results


def get_tokens_count(tokens: Iterable[Token]) -> Dict[Token, int]:
    count: Dict[Token, int] = {}
    # Dictionary used to keep track of lemmatized, lowercase variations of tokens (they are considered the same), while
    # preserving one token's information in the returned dictionary
    normalized_to_token: Dict[str, Token] = {}
    for token in tokens:
        normalized = token.lemma_.lower()
        if normalized in normalized_to_token:
            count[normalized_to_token[normalized]] += 1
        else:
            normalized_to_token[normalized] = token
            count[token] = 1
    return OrderedDict(sorted(count.items(), key=lambda x: x[1], reverse=True))


def analyse_history(urls: List[str]) -> HistoryAnalysisResults:
    history_text = _load_history_text(urls)
    return _analyse_history_text(history_text)


if __name__ == '__main__':
    csv = pd.read_csv('../../datasets/firefox_history.csv')
    urls = csv['URL']
    results = analyse_history(urls)
