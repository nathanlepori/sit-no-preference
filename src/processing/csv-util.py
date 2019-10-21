from typing import List

import pandas as pd

from pandas import DataFrame


def count_words(tokens: List[str]):
    d = {}
    for token in tokens:
        if token in d.keys():
            d[token] += 1
        else:
            d[token] = 1
    return d

if __name__ == '__main__':
