import inspect
import random

from os import PathLike
from pathlib import Path

import spacy

from typing import Dict, Union, Callable, List, Tuple

from spacy.util import compounding, minibatch

import no_preference.processing.ner_training.annotations_loaders as annotations_loaders
from no_preference.processing.ner_training.annotations_loaders import dataturks_loader
from no_preference.lib.util import get_logger, load_model

LOGGER = get_logger(__name__)


def is_annotations_loader(object) -> bool:
    """
    All functions that are declared in the annotations_loaders modules.
    :param object:
    :return:
    """
    return inspect.isfunction(object) and object.__module__ == annotations_loaders.__name__


def get_annotations_loaders() -> List[Tuple[str, Callable]]:
    return inspect.getmembers(annotations_loaders, predicate=is_annotations_loader)


def train_ner(model: Union[str, PathLike], training_data: Dict, output_model: str = None, lang: str = 'en',
              num_iter: int = 100):
    # If not specified otherwise, output onto the starting model
    if output_model is None:
        output_model = model
    try:
        nlp = load_model(model)
    except OSError:
        nlp = spacy.blank(lang)
        blank_model = True
        LOGGER.info(f'Created blank model {model}')
    else:
        blank_model = False
        LOGGER.info(f'Loaded existing model {model}')

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    # add labels
    for _, annotations in training_data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):  # only train NER
        # reset and initialize the weights randomly – but only if we're
        # training a new model
        if blank_model:
            nlp.begin_training()
        LOGGER.info(f'Beginning {num_iter} iterations of training.')
        for itn in range(num_iter):
            random.shuffle(training_data)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(training_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            LOGGER.info(f'{itn + 1}/{num_iter} iterations done.')

    # save model
    output_dir = Path(output_model)
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.to_disk(output_dir)
    LOGGER.info(f'Saved model to {output_dir}')


def test_model(model: Union[str, PathLike], text):
    nlp = load_model(model)
    doc = nlp(text)

    return map(lambda ent: (ent.text, ent.start_char, ent.end_char, ent.label_), doc.ents)


if __name__ == '__main__':
    train_ner(
        '../../../data/models/smash_bros_twitter',
        dataturks_loader('../../../data/annotated_training_data/smash_bros_twitter_annotated.json'),
        num_iter=200
    )
