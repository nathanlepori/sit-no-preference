import types
from typing import Dict, Any, Union, List, Optional, Callable

from PyInquirer import prompt as _prompt

Questions = Union[List[Dict[str, Any]], Dict[str, Any]]
Next = Optional[Union[Questions, Callable, List[Callable]]]


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
    answers = _prompt(questions)
    all_answers = {}
    for name, answer in answers.items():
        next = get_next(questions, answer, name)
        ret = call_next(next)
        if ret:
            all_answers[name] = ret
        else:
            all_answers[name] = answer
    return all_answers


if __name__ == '__main__':
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
