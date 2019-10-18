from collections import OrderedDict
from typing import Iterable, Dict

from spacy.tokens.doc import Doc
from spacy.tokens.token import Token

from src.processing.browser_history import PUNCTUATION


def _is_relevant_token(token: Token) -> bool:
    """
    Returns whether the token is relevant, aka not a stop-word, not punctuation, not newline, and not empty or
    whitespace.
    :param token:
    :return:
    """
    return not token.is_stop and len(token.text.strip()) != 0 and token.text not in PUNCTUATION


def filter_tokens(doc: Doc):
    """
    Filters irrelevant tokens and returns a list of non punctuation, non stop-words, relevant tokens.
    :param doc:
    :return:
    """
    return list(filter(_is_relevant_token, doc))


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
