import types
from datetime import datetime
from functools import partial
from glob import glob
from inspect import signature
from os import path
from typing import Dict, Any, Union, List, Optional, Callable, Iterator

from PyInquirer import prompt as _prompt

from no_preference.lib.util import get_data_dir

Questions = Union[List[Dict[str, Any]], Dict[str, Any]]
Next = Optional[Union[Questions, Callable, List[Callable]]]


def is_datetime(a: str, required: bool = True):
    if not required and not a:
        return True
    else:
        try:
            datetime.fromisoformat(a)
            return True
        except ValueError as e:
            # Return error message
            return str(e)


def to_datetime(a: str, required: bool = True):
    if not required and not a:
        return None
    else:
        datetime.fromisoformat(a)


NAMED_VALIDATE_FUNCTIONS = {
    'required': lambda a: True if a else 'Input is required',
    'is_datetime': is_datetime,
    'is_datetime_or_none': lambda a: is_datetime(a, False)
}
NAMED_FILTER_FUNCTIONS = {
    'to_int': lambda a: int(a),
    'to_datetime': to_datetime,
    'to_datetime_or_none': lambda a: to_datetime(a, False)
}


def _replace_named_functions(questions: Questions):
    """
    Replaces named functions with respective lambda for questions provided.
    :param questions:
    :return:
    """
    if type(questions) is list:
        questions = [_replace_named_functions(question) for question in questions]
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


def _add_back_button(questions: Questions, previous_questions: Questions = None):
    """
    Adds a back button, if necessary, pointing back to the outer set of questions.
    :param questions:
    :param previous_questions:
    :return:
    """
    if type(questions) is list:
        # List of questions
        for q in questions:
            return _add_back_button(q, previous_questions)
    else:
        # One single question
        question: Dict[str, any] = questions

        if question['type'] != 'list' and question['type'] != 'rawlist':
            # Not supported for non-list questions yet
            return question

        if 'back' in question:
            back_name = 'Back...'
            back = question['back']

            # Grab the name of the back button, if provided
            if type(back) is str:
                back_name = back
            elif type(back) is dict and 'name' in back:
                # Different caption provided
                back_name = back['name']

            back_choice = {
                'name': back_name
            }

            if previous_questions is None:
                if callable(back):
                    # Back provided as function
                    back_choice['next'] = back
                elif type(back) is dict:
                    # Back value provided as dict containing a different caption and 'next'
                    back_choice['next'] = back['next']
            else:
                back_choice['next'] = previous_questions

            # Append the button to the list of choices
            question['choices'].append(back_choice)

        return question


def _get_next(questions: Questions, answers: Union[str, List[str]], name: str = None) -> Next:
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
        next_ = []
        for answer in answers:
            try:
                # Choice name should also be unique
                # If there's a filter, extract it to test answers
                if 'filter' in question:
                    filter_ = question['filter']
                else:
                    # Otherwise use passthrough
                    filter_ = lambda a: a
                next_.append([choice['next'] for choice in question['choices'] if
                              type(choice) is dict and 'next' in choice and filter_(choice['name']) == answer][0])
            except IndexError:
                pass
        if len(next_) == 0:
            next_ = None
    else:
        # Single answers
        answer = answers
        try:
            # Choice name should also be unique
            # If there's a filter, extract it to test answers
            if 'filter' in question:
                filter_ = question['filter']
            else:
                # Otherwise use passthrough
                filter_ = lambda a: a
            next_ = [choice['next'] for choice in question['choices'] if
                     # Use filter before comparison to avoid not matching filtered value
                     type(choice) is dict and 'next' in choice and filter_(choice['name']) == answer][0]
        except IndexError:
            next_ = None
    return next_


def _call_next(next_: Next, previous_answers: Dict[str, Any], previous_questions: Questions):
    if not next_:
        return
    if type(next_) is list:
        if all(type(n) is dict for n in next_):
            # A list of questions is provided -> call one after the other and using the questions name, collect answers
            # in a dictionary. This is necessary instead of just passing on the whole list to execute all next
            # callbacks in the right order
            res = {}
            for n in next_:
                res[n['name']] = _call_next(n, previous_answers, previous_questions)
        else:
            # A list of functions (or mixed, ⚠ not supported) is provided -> just collect in a list
            res = []
            for n in next_:
                res.append(_call_next(n, previous_answers, previous_questions))
        return res
    else:
        if callable(next_):
            if isinstance(next_, partial):
                # Partials behave slightly differently, the remaining arguments are stored in a tuple. signature()
                # would return the initial function's arguments which is not what we want
                params = next_.args
                num_params = len(params)
            else:
                params = signature(next_).parameters
                num_params = len(params)
            if num_params == 0:
                return next_()
            else:
                # Create back callback with prompt pointing to previous questions
                back = partial(prompt, questions=previous_questions)
                if num_params == 1:
                    if 'previous_answers' in params:
                        # Call next passing the previous answers to the callback
                        return next_(previous_answers)
                    elif 'back' in params:
                        return next_(back)
                elif num_params == 2:
                    return next_(previous_answers, back)
        else:
            # Else call recursively with a new set of questions
            return prompt(next_)


def prompt(questions: Questions) -> Dict[str, Any]:
    """
    Improved PyInquirer prompt function accepting 'next' key for nested menus, as well as other quality-of-life
    improvements.
    ⚠ When returning single question answers, the returned dictionary will be simplified to a string. Also works for
    nested questions.
    :param questions:
    :return:
    """
    questions = _replace_named_functions(questions)
    questions = _add_back_button(questions)
    answers = _prompt(questions)
    all_answers = {}
    for name, answer in answers.items():
        # Record the question's answer to be passed to the next callback
        all_answers[name] = answer
        next_ = _get_next(questions, answer, name)
        ret = _call_next(next_, all_answers, questions)
        if ret:
            # Return both answers from the main question and nested ones
            all_answers[name] = {
                'name': answer,
                'next': ret
            }

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
        'filter': lambda a: a == 'yes',
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
        *,
        name: str,
        message: str,
        dir_: str,
        allow_custom_file: bool = True,
        custom_file_choice_name: str = 'Other...',
        custom_file_message: str = 'Filename:',
        recursive=False
):
    """
    Returns a question dictionary containing a list of files in a directory relative to the data folder.
    :param custom_file_choice_name:
    :param recursive:
    :param custom_file_message:
    :param allow_custom_file:
    :param name:
    :param message:
    :param dir_:
    :return:
    """
    dir_path = path.join(get_data_dir(), dir_)
    # Get all files inside directory, except the directory itself, if using recursive, then make it relative to that
    # folder (remove first part)
    files: Iterator[str] = map(
        lambda p: path.relpath(p, dir_path),
        glob(path.join(dir_path, '**'), recursive=recursive)[1 if recursive else 0:]
    )

    choices: List[Dict[str, Any]] = list(map(
        lambda f: {
            'name': f
        },
        files
    ))

    if allow_custom_file:
        choices.append({
            'name': custom_file_choice_name,
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


def data_files_prompt(
        *,
        name: str,
        message: str,
        dir_: str,
        allow_custom_file: bool = True,
        custom_file_choice_name: str = 'Other...',
        custom_file_message: str = 'What is the name of the file?',
        recursive=False
):
    answer = prompt(data_files_question(
        name=name,
        message=message,
        dir_=dir_,
        allow_custom_file=allow_custom_file,
        custom_file_choice_name=custom_file_choice_name,
        custom_file_message=custom_file_message,
        recursive=recursive
    ))
    # User chose the 'Other...' option -> simplify answer to string as if it was a simple question
    if 'name' in answer and 'next' in answer[name]:
        return answer[name]['next']
    return answer


def datetime_question(name: str, message: str, required: bool = False):
    return {
        'type': 'input',
        'name': name,
        'message': message,
        'validate': 'is_datetime_or_none',
        'filter': 'to_datetime_or_none'
    }


def datetime_prompt(name: str, message: str):
    return prompt(datetime_question(name, message))


if __name__ == '__main__':
    data_files_prompt(
        name='a',
        message='b',
        dir_='models'
    )

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
