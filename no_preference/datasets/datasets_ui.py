from os import path
from typing import Callable

from no_preference.datasets.browser_history import get_chrome_history, get_firefox_history
from no_preference.datasets.facebook import get_facebook_posts
from no_preference.datasets.twitter import get_twitter_timeline
from no_preference.ui.pyinquirer_menu import prompt
from no_preference.util import get_data_dir, get_logger

LOGGER = get_logger(__name__)


def show_running_on_same_machine_warning():
    def show_error_message():
        print(
            'Load the program on the machine you want to collect the evidence for and call this menu again. Exiting now...')
        exit()

    prompt({
        'type': 'list',
        'name': 'running_on_same_machine',
        'message': 'Are you running the software on the machine for which you want to collect the evidence?',
        'choices': [
            'yes',
            {
                'name': 'no',
                'next': show_error_message
            }
        ]
    })


def get_chrome_history_ui():
    # This is gonna exit in case it's not running on the evidence machine
    show_running_on_same_machine_warning()

    dataset_filename = prompt({
        'type': 'input',
        'name': 'dataset_filename',
        'message': "Where should the Chrome history get saved to? If the file doesn't exist it "
                   "will be created, otherwise this it will be overwritten.",
        'validate': lambda a: len(a) > 0,
    })['dataset_filename']

    dataset_filepath = path.join(get_data_dir(), 'datasets', 'history_data', dataset_filename)
    df = get_chrome_history()
    df.to_csv(dataset_filepath, index=False)
    LOGGER.info(f'Saved dataset to {dataset_filepath}')


def get_firefox_history_ui():
    # This is gonna exit in case it's not running on the evidence machine
    show_running_on_same_machine_warning()

    dataset_filename = prompt({
        'type': 'input',
        'name': 'dataset_filename',
        'message': "Where should the Firefox history get saved to? If the file doesn't exist it "
                   "will be created, otherwise it will be overwritten.",
        'validate': lambda a: len(a) > 0,
    })['dataset_filename']

    dataset_filepath = path.join(get_data_dir(), 'datasets', 'history_data', dataset_filename)
    df = get_firefox_history()
    df.to_csv(dataset_filepath, index=False)
    LOGGER.info(f'Saved dataset to {dataset_filepath}')


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
            'validate': lambda a: len(a) > 0,
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
            'validate': lambda a: len(a) > 0,
        },
        {
            'type': 'input',
            'name': 'dataset_filename',
            'message': "Where should the Facebook data get saved to? If the file doesn't exist it "
                       "will be created, otherwise it will be overwritten.",
            'validate': lambda a: len(a) > 0,
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
                'next': get_chrome_history_ui
            },
            {
                'name': 'Firefox history',
                'next': get_firefox_history_ui
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

    # while True:
    #
    #     a_browser = prompt(q_browser)
    #     if a_browser['browser'] == "exit":
    #         break
    #     if a_browser['browser'] == "chrome":
    #         df_browser = get_chrome_history()
    #         output_datasets_name = path.join(get_data_dir(), 'datasets', 'chrome.csv')
    #         a_append_overwrite = prompt(q_append_overwrite)
    #
    #     if a_browser['browser'] == "firefox":
    #         df_browser = get_firefox_history()
    #         output_datasets_name = path.join(get_data_dir(), 'datasets', 'firefox.csv')
    #         a_append_overwrite = prompt(q_append_overwrite)
    #
    #     if a_append_overwrite['integrate'] == "append":
    #         df_browser.to_csv(output_datasets_name, encoding='utf-8', mode='a+', index=False)
    #     if a_append_overwrite['integrate'] == "overwrite":
    #         df_browser.to_csv(output_datasets_name, encoding='utf-8', mode='w+', index=False)
