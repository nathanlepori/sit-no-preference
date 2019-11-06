import no_preference.processing.ner_training.training_ui as training_ui
from no_preference.processing import analysis
from no_preference.ui.pyinquirer_menu import prompt
from no_preference.util import create_data_dir


def init():
    create_data_dir()


def run():
    prompt({
        'type': 'list',
        'name': 'action',
        'message': 'What do you want to do?',
        'choices': [
            {
                'name': 'Get data for profiling',
            },
            {
                'name': 'Train a model',
                'next': training_ui.run
            },
            {
                'name': 'Analyse data',
                'next': analysis.run
            },
            {
                'name': 'Show profiling results',
            }
        ]
    })


if __name__ == '__main__':
    init()
    run()
