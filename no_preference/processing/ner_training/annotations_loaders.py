import json

from no_preference.util import get_logger

LOGGER = get_logger(__name__)


def convert_dataturks_to_spacy(annotations_filepath):
    """
    ############################################  NOTE  ########################################################
    #
    #           Creates NER training data in Spacy format from JSON downloaded from Dataturks.
    #
    #           Outputs the Spacy training data which can be used for Spacy training.
    #
    ############################################################################################################
    :param annotations_filepath:
    :return:
    """
    try:
        training_data = []
        with open(annotations_filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            data = json.loads(line)
            text = data['content']
            entities = []
            for annotation in data['annotation'] or []:
                # only a single point in text annotation.
                point = annotation['points'][0]
                labels = annotation['label']
                # handle both list of labels or a single label.
                if not isinstance(labels, list):
                    labels = [labels]

                for label in labels:
                    # dataturks indices are both inclusive [start, end] but spacy is not [start, end)
                    entities.append((point['start'], point['end'] + 1, label))

            training_data.append((text, {"entities": entities}))

        return training_data
    except Exception as e:
        LOGGER.exception("Unable to process " + annotations_filepath + "\n" + "error = " + str(e))
        return None
