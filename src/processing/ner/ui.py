from src.data_sources.twitter import get_following, get_tweets_for_training
from src.ui.pyinquirer_menu import prompt


def twitter_training_data_ui():
    profiled_screen_name_question = {
        'type': 'input',
        'name': 'profiled_screen_name',
        'message': "What's the Twitter screen name of the person you're profiling (string after '@')?"
    }
    profiled_screen_name = prompt(profiled_screen_name_question)['profiled_screen_name']

    # following = get_following(profiled_screen_name)
    following = [
        'hearthsono',
        'Dark_Wizzy_',
        'zyneoph',
        'Terrarian800',
        'megajon_1',
        'PSI_4ce',
        'DJliveYoshi',
        '__Inf1nite__',
        'Thunder_Armads',
        'Exalted_eye',
        'SkarfeltSSB',
        'HugS86',
        'ViciousVish'
    ]
    training_data_questions = [
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
    ]
    training_data_answers = prompt(training_data_questions)
    return get_tweets_for_training(training_data_answers['training_data_screen_names'],
                                   num_tweets=training_data_answers['training_data_num_tweets'])


def run():
    questions = [{
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
            'Test a model',
        ]
    }]

    answers = prompt(questions)
    print(answers)


if __name__ == '__main__':
    run()
