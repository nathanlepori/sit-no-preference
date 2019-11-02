import random
from pathlib import Path

import spacy

from typing import Dict

from spacy.util import compounding, minibatch

from src.processing.ner.training.convert_dataturks_to_spacy import convert_dataturks_to_spacy
from src.util import get_logger

LOGGER = get_logger(__file__)


def train_ner(model: str, training_data: Dict, output_model: str = None, lang: str = 'en', num_iter: int = 100):
    # If not specified otherwise, output onto the starting model
    if output_model is None:
        output_model = model
    try:
        nlp = spacy.load(model)
        blank_model = False
        LOGGER.info(f'Loaded existing model {model}')
    except OSError as e:
        nlp = spacy.blank(lang)
        blank_model = True
        LOGGER.info(f'Created blank model {model}')

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
    output_dir = Path(model)
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.to_disk(output_dir)
    LOGGER.info(f'Saved model to {output_dir}')


def test_model(model: str, text):
    nlp = spacy.load(model)
    doc = nlp(text)

    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)


if __name__ == '__main__':
    train_ner(
        '../../../../models/smash_bros_twitter',
        convert_dataturks_to_spacy('../../../../datasets/smash_bros_twitter_annotated_2.json'),
        num_iter=200
    )
