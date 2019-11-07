from os import path
from datetime import datetime

import no_preference.datasets.browser_history as browser_history
from no_preference.datasets.facebook import get_facebook_posts
from no_preference.datasets.twitter import get_twitter_timeline
from no_preference.processing.browser_history import load_history
from no_preference.ui.pyinquirer_menu import prompt, yes_no_question, yes_no_prompt
from no_preference.util import get_data_dir, get_logger

LOGGER = get_logger(__name__)


def show_running_on_same_machine_warning():
    def show_error_message():
        print('Load the program on the machine you want to collect the evidence for and call this '
              'menu again. Exiting now...')
        exit()

    yes_no_prompt(
        'running_on_same_machine',
        'Are you running the software on the machine for which you want to collect the evidence?',
        no_next=show_error_message
    )


def get_browser_history_ui(browser: str):
    # This is gonna exit in case it's not running on the evidence machine
    show_running_on_same_machine_warning()

    a_dataset = prompt([
        {
            'type': 'input',
            'name': 'dataset_filename',
            'message': f"Where should the {browser.capitalize()} history get saved to? If the file does not exist it "
                       "will be created, otherwise it will be overwritten.",
            'validate': 'required',
        },
        yes_no_question(
            'load_history',
            'Do you want to also crawl the content of the visited web pages? This operation will take a while...',
            yes_next=[
                {
                    'type': 'input',
                    'name': 'dataset_content_from',
                    'message': 'From what date and time would you like to retrieve the history content (format: ISO '
                               '8601, blank for no lower filtering)?',
                    'filter': 'to_datetime'
                },
                {
                    'type': 'input',
                    'name': 'dataset_content_to',
                    'message': 'From what date and time would you like to retrieve the history content (format: ISO '
                               '8601, blank for no upper filtering)?',
                    'filter': 'to_datetime'
                },
                {
                    'type': 'input',
                    'name': 'dataset_content_filename',
                    'message': f"Where should the {browser.capitalize()} history content get saved to? If the "
                               "file doesn't exist it will be created, otherwise it will be overwritten.",
                    'validate': 'required'
                }
            ]
        ),
    ])

    dataset_filepath = path.join(get_data_dir(), 'datasets', 'history_data', a_dataset['dataset_filename'])
    history = getattr(browser_history, f'get_{browser}_history')()
    history.to_csv(dataset_filepath, index=False)
    LOGGER.info(f'Saved dataset to {dataset_filepath}')

    # Load history content
    if a_dataset['load_history']['name']:
        dataset_content_filepath = path.join(get_data_dir(), 'datasets', 'history_data',
                                             a_dataset['load_history']['next']['dataset_content_filename'])
        history_content = load_history(
            history,
            a_dataset['load_history']['next']['dataset_content_from'],
            a_dataset['load_history']['next']['dataset_content_to']
        )
        history_content.to_csv(dataset_content_filepath, index=False)
        LOGGER.info(f'Saved dataset to {dataset_content_filepath}')


def get_twitter_timeline_ui():
    a_dataset = prompt([
        {
            'type': 'input',
            'name': 'profiled_screen_name',
            'message': "What's the Twitter screen name of the person you're profiling (string after '@')?"
        },
        {
            'type': 'input',
            'name': 'dataset_filename',
            'message': "Where should the Twitter timeline get saved to? If the file doesn't exist it "
                       "will be created, otherwise it will be overwritten.",
            'validate': 'required'
        }
    ])

    dataset_filepath = path.join(get_data_dir(), 'datasets', 'social_data', a_dataset['dataset_filename'])
    twitter_timeline = get_twitter_timeline(a_dataset['profiled_screen_name'])
    twitter_timeline.to_csv(dataset_filepath, index=False)
    LOGGER.info(f'Saved dataset to {dataset_filepath}')


def get_facebook_data_ui():
    print('Refer to https://www.facebook.com/help/212802592074644 on how to download data from a '
          'Facebook account. You will need the login credentials of the person you are profiling. ')
    input('Press enter when you are ready to proceed...')

    a_dataset = prompt([
        {
            'type': 'input',
            'name': 'facebook_data_dir',
            'message': "Where is your Facebook data directory located?",
            'validate': 'required'
        },
        {
            'type': 'input',
            'name': 'dataset_filename',
            'message': "Where should the Facebook data get saved to? If the file doesn't exist it "
                       "will be created, otherwise it will be overwritten.",
            'validate': 'required'
        }
    ])

    dataset_filepath = path.join(get_data_dir(), 'datasets', 'social_data', a_dataset['dataset_filename'])
    posts = get_facebook_posts(a_dataset['facebook_data_dir'])
    posts.to_csv(dataset_filepath, index=False)
    LOGGER.info(f'Saved dataset to {dataset_filepath}')


def run():
    q_data_sources = {
        'type': 'checkbox',
        'name': 'data_source',
        'message': 'Select the data you want to import',
        'choices': [
            {
                'name': 'Chrome history',
                'next': lambda _: get_browser_history_ui('chrome')
            },
            {
                'name': 'Firefox history',
                'next': lambda _: get_browser_history_ui('firefox')
            },
            {
                'name': 'Twitter timeline',
                'next': get_twitter_timeline_ui
            },
            {
                'name': 'Facebook posts',
                'next': get_facebook_data_ui
            }
        ]
    }
    prompt(q_data_sources)
