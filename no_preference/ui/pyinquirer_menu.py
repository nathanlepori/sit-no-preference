import os
import types
from os import PathLike
from typing import Dict, Any, Union, List, Optional, Callable

from PyInquirer import prompt as _prompt

from no_preference.util import get_data_dir

Questions = Union[List[Dict[str, Any]], Dict[str, Any]]
Next = Optional[Union[Questions, Callable, List[Callable]]]

NAMED_VALIDATE_FUNCTIONS = {
    'required': lambda a: len(a) > 0
}
NAMED_FILTER_FUNCTIONS = {
    'to_int': lambda a: int(a)
}

def replace_named_functions(questions: Questions):
    """
    Replaces named functions with respective lambda for questions provided.
    :param questions:
    :return:
    """
    if type(questions) is list:
        questions = [replace_named_functions(question) for question in questions]
    else:
        question = questions
        # Replace validate and filter functions if values are strings and they are present in the respective replacement
        # dictionaries
        if 'validate' in question and \
                type(question['validate']) is str and \
                question['validate'] in NAMED_VALIDATE_FUNCTIONS:
            question['validate'] = NAMED_VALIDATE_FUNCTIONS[question['validate']]

        if 'filter' in question and \
                type(question['filter']) is str and \
                question['filter'] in NAMED_FILTER_FUNCTIONS:
            question['filter'] = NAMED_FILTER_FUNCTIONS[question['filter']]
    return questions


def get_next(questions: Questions, answers: Union[str, List[str]], name: str = None) -> Next:
    question: Optional[Dict[str, Any]]
    if type(questions) is list:
        # Is a list of questions
        # There should only be one question for a given name
        try:
            question = [question for question in questions if question['name'] == name][0]
        except IndexError:
            question = None
    else:
        # Is a single question
        question = questions

    # No question with such name or questions without choices (unsupported)
    if not question or 'choices' not in question:
        return None

    if type(answers) is list:
        # Checkbox and other list returning questions
        next = []
        for answer in answers:
            try:
                # Choice name should also be unique
                next.append([choice['next'] for choice in question['choices'] if
                             type(choice) is dict and 'next' in choice and choice['name'] == answer][0])
            except IndexError:
                pass
        if len(next) == 0:
            next = None
    else:
        # Single answers
        answer = answers
        try:
            # Choice name should also be unique
            next = [choice['next'] for choice in question['choices'] if
                    type(choice) is dict and 'next' in choice and choice['name'] == answer][0]
        except IndexError:
            next = None
    return next


def call_next(next: Next):
    if not next:
        return
    if type(next) is list:
        if all(type(n) is dict for n in next):
            # A list of questions is provided -> using the questions name, collect answers in a dictionary
            res = {}
            for n in next:
                res[n['name']] = call_next(n)
        else:
            # A list of functions (or mixed, ⚠ not supported) is provided -> just collect in a list
            res = []
            for n in next:
                res.append(call_next(n))
        return res
    else:
        if isinstance(next, (types.FunctionType, types.BuiltinFunctionType, types.LambdaType)):
            if next.__name__ == '<lambda>':
                # If next is a lambda, call it with the unused argument
                return next(None)
            else:
                # If it's a function, just call it
                return next()
        else:
            # Else call recursively with a new set of questions
            return prompt(next)


def prompt(questions: Questions):
    """
    Improved PyInquirer prompt function accepting 'next' key for nested menus, as well as other quality-of-life
    improvements.
    :param questions:
    :return:
    """
    questions = replace_named_functions(questions)
    answers = _prompt(questions)
    all_answers = {}
    for name, answer in answers.items():
        next = get_next(questions, answer, name)
        ret = call_next(next)
        if ret:
            # Return both answers from the main question and nested ones
            all_answers[name] = {
                'name': answer,
                'next': ret
            }
        else:
            all_answers[name] = answer

    # Single question case -> just return answer, not dictionary
    top_answers_names = list(all_answers.keys())
    if len(top_answers_names) == 1 and type(all_answers[top_answers_names[0]]) is not dict:
        return all_answers[top_answers_names[0]]

    return all_answers


def yes_no_question(name: str, message: str, yes_next=None, no_next=None):
    """
    Returns a yes/no question dictionary with the provided name, message and optional next prompts.
    :param name:
    :param message:
    :param yes_next:
    :param no_next:
    :return:
    """
    return {
        'type': 'list',
        'name': name,
        'message': message,
        'choices': [
            {
                'name': 'yes',
                'next': yes_next
            },
            {
                'name': 'no',
                'next': no_next
            }
        ]
    }


def yes_no_prompt(name: str, message: str, yes_next=None, no_next=None):
    """
    Starts a yes/no prompt with the provided name, message and optional next prompts.
    :param name:
    :param message:
    :param yes_next:
    :param no_next:
    :return:
    """
    return prompt(yes_no_question(name, message, yes_next, no_next))


def data_files_question(
        name: str,
        message: str,
        dir: str,
        allow_custom_file: bool = True,
        custom_file_message: str = 'What is the name of the file?'):
    """
    Returns a question dictionary containing a list of files in a directory relative to the data folder.
    :param custom_file_message:
    :param allow_custom_file:
    :param name:
    :param message:
    :param dir:
    :return:
    """
    choices: List[Union[str, Dict[str, Any]]] = os.listdir(os.path.join(get_data_dir(), dir))

    if allow_custom_file:
        choices.append({
            'name': 'Other...',
            'next': {
                'type': 'input',
                'name': 'filename',
                'message': custom_file_message,
                'validate': 'required'
            }
        })
    return {
        'type': 'list',
        'name': name,
        'message': message,
        'choices': choices
    }


def data_files_prompt(name: str, message: str, dir: str, allow_custom_file: bool = True):
    return prompt(data_files_question(name, message, dir, allow_custom_file))


if __name__ == '__main__':
    data_files_prompt('a', 'b', 'models')

    questions = {
        'type': 'list',
        'name': 'action',
        'message': 'What do you want to do?',
        'choices': [
            {
                'name': 'Get data for annotation',
                'next': {
                    'type': 'checkbox',
                    'message': 'Where do you want to get the training data from?',
                    'name': 'training_data_sources',
                    'choices': [
                        {
                            'name': 'Twitter'
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
    }

    answers = prompt(questions)
    print(answers)
