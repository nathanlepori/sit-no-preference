import logging
from typing import List


def flatten(l: List[List]) -> List:
    return [item for sublist in l for item in sublist]


def get_logger(name: str, level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

    # Only for debug purposes
    logger.setLevel(level)
    return logger
