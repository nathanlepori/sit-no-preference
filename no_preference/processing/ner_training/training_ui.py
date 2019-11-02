import itertools
from os import path

from no_preference.data_sources.twitter import get_following, get_tweets_for_training
from no_preference.processing.ner_training.training import test_model, train_ner, get_annotations_loaders
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


def train_model_ui():
    base_model_name = prompt({
        'type': 'input',
        'name': 'base_model_name',
        'message': "What is the name of the model you want to train? If it doesn't exists it will be created.",
        'validate': lambda a: len(a) > 0,
    })['base_model_name']

    annotations_loaders = get_annotations_loaders()
    training_answers = prompt([
        {
            'type': 'input',
            'name': 'training_data_filename',
            'message': "What is the name of the annotated training data file you want to train this model against?",
            'validate': lambda a: len(a) > 0,
        },
        {
            'type': 'list',
            'name': 'annotations_loader',
            'message': 'What annotation loader do you want to use to load the file?',
            'choices': map(lambda loader: loader[0], annotations_loaders),
            'filter': lambda loader_name: [loader[1] for loader in annotations_loaders if loader[0] == loader_name][0]
        },
        {
            'type': 'input',
            'name': 'output_model_name',
            'message': "Where do you want to save the trained model? If the model already exists it will be overridden.",
            'default': base_model_name,
            'validate': lambda a: len(a) > 0,
        },
        {
            'type': 'input',
            'name': 'num_iter',
            'message': "How many iteration should this training last?",
            'default': '100',
            'validate': lambda a: a.isdigit() and int(a) > 0,
            'filter': lambda a: int(a)
        }
    ])

    annotations_loaders = training_answers['annotations_loader']
    training_data_filename = path.join(get_data_dir(), 'annotated_training_data', training_answers['training_data_filename'])
    output_model_name = path.join(get_data_dir(), 'models', training_answers['output_model_name'])
    train_ner(model=base_model_name,
              training_data=annotations_loaders(training_data_filename),
              output_model=output_model_name,
              num_iter=training_answers['num_iter'])


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
            {
                'name': 'Train a model',
                'next': train_model_ui
            },
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
