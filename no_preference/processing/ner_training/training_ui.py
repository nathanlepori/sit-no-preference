import itertools
from os import path

from no_preference.data_sources.twitter import get_following, get_tweets_for_training
from no_preference.processing.ner_training.training import test_model
from no_preference.ui.pyinquirer_menu import prompt
from no_preference.util import get_data_dir, get_logger

LOGGER = get_logger(__name__)


def twitter_training_data_ui():
    profiled_screen_name = prompt({
        'type': 'input',
        'name': 'profiled_screen_name',
        'message': "What's the Twitter screen name of the person you're profiling (string after '@')?"
    })['profiled_screen_name']

    following = get_following(profiled_screen_name)
    training_data_answers = prompt([
        {
            'type': 'input',
            'name': 'training_data_num_tweets',
            'message': "How many Tweets do you want to download for the training data?",
            'default': '60',
            'validate': lambda a: a.isdigit() and int(a) > 0,
            'filter': lambda a: int(a)
        },
        {
            'type': 'checkbox',
            'name': 'training_data_screen_names',
            'message': f'Which of the users followed by {profiled_screen_name} do you want to get data from?',
            'choices': map(lambda f: {
                'name': f
            }, following),
            'pageSize': 10
        }
    ])
    return get_tweets_for_training(training_data_answers['training_data_screen_names'],
                                   num_tweets=training_data_answers['training_data_num_tweets'])


def save_training_data(training_data):
    training_data_filename = prompt({
        'type': 'input',
        'name': 'training_data_filename',
        'message': "Where should the training data get saved to? If the file doesn't exist it will be created, "
                   "otherwise this training data will be appended.",
        'validate': lambda a: len(a) > 0,
    })['training_data_filename']
    with open(path.join(get_data_dir(), 'training_data', training_data_filename), 'a', encoding='utf-8') as f:
        f.writelines(map(lambda l: f'{l}\n', training_data))
    LOGGER.info(f'Successfully saved training data {training_data_filename}.')


def run():
    questions = {
        'type': 'list',
        'name': 'action',
        'message': 'What do you want to do?',
        'choices': [
            {
                'name': 'Get data for annotation',
                'next': {
                    'type': 'checkbox',
                    'name': 'training_data_sources',
                    'message': 'Where do you want to get the training data from?',
                    'choices': [
                        {
                            'name': 'Twitter',
                            'next': twitter_training_data_ui
                        },
                        {
                            'name': 'Facebook',
                            'disabled': 'Not supported yet'
                        }
                    ]
                }
            },
            {
                'name': 'Annotate data using Prodigy',
                'disabled': 'Not supported yet'
            },
            'Train a model',
            {
                'name': 'Test a model',
                'next': {
                    'type': 'input',
                    'name': 'test_model_name',
                    'message': "What is the name of the model you want to test?",
                    'validate': lambda a: len(a) > 0,
                }
            }
        ]
    }

    action = prompt(questions)['action']

    if 'training_data_sources' in action:
        # Get data for annotation case
        # Chain texts from all sources
        training_data = itertools.chain.from_iterable(action['training_data_sources'])
        save_training_data(training_data)
    elif 'test_model_name' in action:
        # Test model case
        test_model_name = action['test_model_name']

        test_model_text = prompt({
            'type': 'input',
            'name': 'test_model_text',
            'message': "What is the text you want to test against this model?",
            'validate': lambda a: len(a) > 0,
        })['test_model_text']

        ents = test_model(test_model_name, test_model_text)
        for ent in ents:
            print(*ent)


if __name__ == '__main__':
    run()
