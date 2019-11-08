import no_preference.processing.ner_training.training_ui as training_ui
from no_preference.processing.analysis import analysis_ui
from no_preference.datasets import datasets_ui
from no_preference.lib.pyinquirer_menu import prompt
from no_preference.lib.util import create_data_dir
from no_preference.results_gui import gui



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
                'next': datasets_ui.run
            },
            {
                'name': 'Train a model',
                'next': training_ui.run
            },
            {
                'name': 'Analyse data',
                'next': analysis_ui.run
            },
            {
                'name': 'Show profiling results',
                'next': gui.run
            }
        ]
    })


if __name__ == '__main__':
    init()
    run()
