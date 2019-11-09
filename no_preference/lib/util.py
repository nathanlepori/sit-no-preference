import logging
import os
import sys
from typing import List, Union

import spacy
from spacy.language import Language

import no_preference

MAIN_EXECUTABLE_FILENAME = 'no_preference.py'


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


def create_data_dir():
    dirs = [
        'training_data',
        'annotated_training_data',
        'models',
        'datasets/history_data',
        'datasets/social_data',
        'results'
    ]
    for d in dirs:
        os.makedirs(os.path.join(get_project_root(), 'data', d), exist_ok=True)


def get_project_root():
    main_module = sys.modules['__main__']

    # If running from the main executable just get his path
    if os.path.basename(main_module.__file__) == MAIN_EXECUTABLE_FILENAME:
        return os.path.dirname(main_module.__file__)
    # Otherwise go up one directory from the main package
    return os.path.abspath(os.path.join(os.path.dirname(no_preference.__file__), '..'))


def get_data_dir():
    return os.path.join(get_project_root(), 'data')


def load_model(name: Union[str, os.PathLike]) -> Language:
    """
    Load either a built-in or downloaded SpaCy model or a custom one from the data directory.
    :param name: Name or path of the model to load.
    :return: Loaded model instance or None if not found.
    """
    try:
        nlp = spacy.load(name)
    except OSError:
        nlp = spacy.load(os.path.join(get_data_dir(), 'models', name))
    return nlp
