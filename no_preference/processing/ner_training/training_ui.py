import itertools
from os import path

from no_preference.datasets.twitter import get_following, get_tweets_for_training
from no_preference.processing.ner_training.training import test_model, train_ner, get_annotations_loaders
from no_preference.lib.pyinquirer_menu import prompt, data_files_question, data_files_prompt
from no_preference.lib.util import get_data_dir, get_logger

LOGGER = get_logger(__name__)


def twitter_training_data_ui():
    profiled_screen_name = prompt({
        'type': 'input',
        'name': 'profiled_screen_name',
        'message': "What's the Twitter screen name of the person you're profiling (string after '@')?"
    })

    following = get_following(profiled_screen_name)
    a_training_data = prompt([
        {
            'type': 'input',
            'name': 'training_data_num_tweets',
            'message': "How many Tweets do you want to download for the training data?",
            'default': '60',
            'validate': lambda a: a.isdigit() and int(a) > 0,
            'filter': 'to_int'
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
    return get_tweets_for_training(a_training_data['training_data_screen_names'],
                                   num_tweets=a_training_data['training_data_num_tweets'])


def save_training_data(training_data):
    training_data_filename = prompt({
        'type': 'input',
        'name': 'training_data_filename',
        'message': "Where should the training data get saved to? If the file doesn't exist it will be created, "
                   "otherwise this training data will be appended.",
        'validate': 'required'
    })
    with open(path.join(get_data_dir(), 'training_data', training_data_filename), 'a', encoding='utf-8') as f:
        f.writelines(map(lambda l: f'{l}\n', training_data))
    LOGGER.info(f'Successfully saved training data {training_data_filename}.')


def train_model_ui():
    base_model_name = data_files_prompt(
        'base_model_name',
        'Select a model to test.',
        'models',
        allow_custom_file=True,
        custom_file_message="What is the name of the model you want to train? If it doesn't exists it will be created."
    )

    annotations_loaders = get_annotations_loaders()
    a_training = prompt([
        {
            'type': 'input',
            'name': 'training_data_filename',
            'message': "What is the name of the annotated training data file you want to train this model against?",
            'validate': 'required',
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
            'validate': 'required'
        },
        {
            'type': 'input',
            'name': 'num_iter',
            'message': "How many iteration should this training last?",
            'default': '100',
            'validate': lambda a: a.isdigit() and int(a) > 0,
            'filter': 'to_int'
        }
    ])

    annotations_loaders = a_training['annotations_loader']
    training_data_filename = path.join(get_data_dir(), 'annotated_training_data', a_training['training_data_filename'])
    output_model_name = path.join(get_data_dir(), 'models', a_training['output_model_name'])
    train_ner(model=base_model_name,
              training_data=annotations_loaders(training_data_filename),
              output_model=output_model_name,
              num_iter=a_training['num_iter'])


def run():
    q_training = {
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
                'next': [
                    data_files_question(
                        'test_model_name',
                        'Select a model to test.',
                        'models',
                        allow_custom_file=True,
                        custom_file_message='What is the name of the model you want to test?'
                    ),
                    {
                        'type': 'input',
                        'name': 'test_model_text',
                        'message': "What is the text you want to test against this model?",
                        'validate': 'required'
                    }
                ]
            }
        ]
    }

    action = prompt(q_training)['action']

    if action['name'] == 'Get data for annotation':
        # Get data for annotation case
        # Chain texts from all sources
        training_data = itertools.chain.from_iterable(action['next']['training_data_sources']['next'])
        save_training_data(training_data)
    elif action['name'] == 'Test a model':
        # Test model case
        test_model_name = action['next']['test_model_name']
        test_model_text = action['next']['test_model_text']

        ents = test_model(test_model_name, test_model_text)
        for ent in ents:
            print(*ent)


if __name__ == '__main__':
    run()
