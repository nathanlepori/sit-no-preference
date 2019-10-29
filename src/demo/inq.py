# # -*- coding: utf-8 -*-
# """
# * Input prompt example
# * run example by writing `python example/input.py` in your console
# """
# from __future__ import print_function, unicode_literals
import regex
from pprint import pprint

from PyInquirer import style_from_dict, Token, prompt

from src.demo.defaults import *
from src.demo.spacyNLP import *
from src.demo.venn import *

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

q_file_loc = [
    {
        'type': 'input',
        'name': 'file_A',
        'message': 'Please indicate file_A\'s name and location >',
    },
    {
        'type': 'input',
        'name': 'file_B',
        'message': 'Please indicate file_B\'s name and location >',
    },
]

q_file_A_request = [
    {
        'type': 'input',
        'name': 'filename',
        'message': 'Please indicate file_A\'s name and location to save content as >',
    }
]

q_file_B_request = [
    {
        'type': 'input',
        'name': 'filename',
        'message': 'Please indicate file_B\'s name and location to save content as >',
    }
]

q_label = [
    {
        'type': 'rawlist',
        'name': 'venn',
        'message': 'Select the type of venn diagram for token with label tag >',
        'choices': [
            'display',
            'intersect',
            'symmetric_difference',
            'union',
            'modify',
            'math',
            'term_association',
            'exit'
        ]
    },
]

q_file_select = [
    {
        'type': 'rawlist',
        'name': 'file_selection',
        'message': 'Please indicate which set of data to use >',
        'choices': [
            'file_A',
            'file_B',
            'both'
        ]
    },
]

q_math_value = [
    {
        'type': 'input',
        'name': 'value',
        'message': 'Please enter value to determine frequency by date >',
    }
]

q_filter = [
    {
        'type': 'rawlist',
        'name': 'modify',
        'message': 'Select the type of modification to the Data >',
        'choices': [
            'filter',
            'strip',
            'exit'
        ]
    },
]

q_filter_value = [
    {
        'type': 'input',
        'name': 'value',
        'message': 'Please enter value to filter or strip >',
    },
]

q_start = [
    {
        'type': 'rawlist',
        'name': 'start',
        'message': 'Select option >',
        'choices': [
            'charlyn',
            'guobao',
            'nathan',
            'gary',
            'load_file',
            'spacy',
        ]
    },
]

q_math = [
    {
        'type': 'rawlist',
        'name': 'math',
        'message': 'Select option for math >',
        'choices': [
            'display',
            'counter',
            'frequency_By_Date',
            'save',
            'exit'
        ]
    },
]

q_assoc = [
    {
        'type': 'rawlist',
        'name': 'assoc',
        'message': 'Select option for term association >',
        'choices': [
            'detached',
            'attached',
        ]
    },
]

q_assoc_method = [
    {
        'type': 'rawlist',
        'name': 'method',
        'message': 'Select option to add a term or run >',
        'choices': [
            'insert_term',
            'run',
            'exit',
        ]
    },
]

q_text_tag = [
    {
        'type': 'rawlist',
        'name': 'text_tag',
        'message': 'Please indicate either text or tag to use >',
        'choices': [
            'text',
            'tag'
        ]
    }
]

q_assoc_term = [
    {
        'type': 'rawlist',
        'name': 'text_tag',
        'message': 'Please indicate term association is based on which option >',
        'choices': [
            'text',
            'tag'
        ]
    },
    {
        'type': 'input',
        'name': 'value',
        'message': 'Please enter value to for term association >',
    },
]


def _readfile():  # temporary function, might need to remove after using nathan's code
    if a_file_loc['file_A'] == '':
        filenameA = defaultFileA()
    else:
        filenameA = a_file_loc['file_A']
    read = readFile(filenameA)
    df = pd.DataFrame(read, columns=[columnName, defaultDateColumn()])  # impt to match columns

    if a_file_loc['file_B'] == '':
        filenameB = defaultFileB()
    else:
        filenameB = a_file_loc['file_B']
    read2 = readFile(filenameB)
    df2 = pd.DataFrame(read2, columns=[columnNameB, defaultDateColumn()])  # impt to match columns

    return df, df2


def writeFile(content, filename):  # write to file.
    f = open(filename, "w+")
    f.write(str(content))
    f.close()


def _process_selection_label(df, columnName, df2, columnNameB):
    """ :return df, df2:

    function to process the user selections made in the command line user interfaces
        this overs the intersect -> vennIntersectTextTag,
            symmetric difference -> vennSymmetricDifTextTag and
            union -> vennUnion() functions
            from venn.py
    """
    if a_label['venn'] == 'intersect' or 'symmetric_difference' or 'union':
        a_text_tag = prompt(q_text_tag)  # used to determine which element in a list to use
        if a_text_tag['text_tag'] == 'text':  # eg. to choose either value or text/tage in the list [value,text/tag]
            textTagOption = 0
        elif a_text_tag['text_tag'] == 'tag':
            textTagOption = 1

    if a_label['venn'] == 'intersect':
        vennIntersectTextTag(df, columnName, df2, columnNameB, textTagOption)
        spacyCleanCell(df, columnName)  # clean empty list from the dataframe
        spacyCleanCell(df2, columnNameB)  # clean empty list from the dataframe
        df = df.reset_index(drop=True)
        df2 = df2.reset_index(drop=True)

    if a_label['venn'] == 'symmetric_difference':
        vennSymmetricDifTextTag(df, columnName, df2, columnNameB, textTagOption)
        spacyCleanCell(df, columnName)
        spacyCleanCell(df2, columnNameB)
        # print("CLEAN ROWWW")
        # spacyCleanRow(df,columnName)
        # spacyCleanRow(df2,columnNameB)
        df = df.reset_index(drop=True)
        df2 = df2.reset_index(drop=True)

    if a_label['venn'] == 'union':
        df = venn.vennUnion(df, df2)
        del df2
        df2 = pd.DataFrame

    return df, df2


def _process_selection_modify(df, columnName, df2, columnNameB):
    """ :return: df, df2

    function to process the user selections made in the command line user interfaces
        this overs the spacyColumnFilterToken() and spacyColumnStripToken() function from spacyNLP.py
    """
    while True:
        a_filter = prompt(q_filter)
        if a_filter['modify'] == 'exit':
            break
        if a_filter['modify'] == 'filter' or 'strip':
            a_text_tag = prompt(q_text_tag)
            if a_text_tag['text_tag'] == 'text':
                textTagOption = 0
            elif a_text_tag['text_tag'] == 'tag':
                textTagOption = 1
            a_filter_value = prompt(q_filter_value)
            value = a_filter_value['value']
            a_file_select = prompt(q_file_select)
            if a_filter['modify'] == 'filter':
                if a_file_select['file_selection'] == 'file_A' or 'both':
                    spacyColumnFilterToken(df, columnName, value, textTagOption)
                if a_file_select['file_selection'] == 'file_B' or 'both':
                    spacyColumnFilterToken(df2, columnNameB, value, textTagOption)

            if a_filter['modify'] == 'strip':
                if a_file_select['file_selection'] == 'file_A' or 'both':
                    spacyColumnStripToken(df, columnName, value, textTagOption)
                if a_file_select['file_selection'] == 'file_B' or 'both':
                    spacyColumnStripToken(df2, columnNameB, value, textTagOption)
            spacyCleanCell(df, columnName)
            spacyCleanCell(df2, columnNameB)
            df = df.reset_index(drop=True)
            df2 = df2.reset_index(drop=True)

    return df, df2


def _process_selection_math(df, columnName, df2, columnNameB):
    """ :return: df, df2

    function to process the user selections made in the command line user interfaces
        this covers over the basic mathematical calculation for the dataframe.
            counting by value or counting value by its date
    """
    countA = []
    countB = []
    while True:
        a_math = prompt(q_math)
        if a_math['math'] == 'exit':
            break
        if a_math['math'] == 'display':
            if len(countA) != 0:
                print("file_A:", end=' ')
                print(countA)
            else:
                print("empty, please run a math method for file_A")
            if len(countB) != 0:
                print("file_B:", end=' ')
                print(countB)
            else:
                print("empty, please run a math method for file_B")
        if a_math['math'] == 'save':
            a_file_select = prompt(q_file_select)
            if a_file_select['file_selection'] == 'file_A' or 'both':
                a_file_A_request = prompt(q_file_A_request)
                filename = a_file_A_request['filename']
                writeFile(countA, filename)
            if a_file_select['file_selection'] == 'file_B' or 'both':
                a_file_B_request = prompt(q_file_B_request)
                filename = a_file_B_request['filename']
                writeFile(countB, filename)

        if a_math['math'] == 'counter' or 'frequency_By_Date':
            a_text_tag = prompt(q_text_tag)
            if a_text_tag['text_tag'] == 'text':
                textTagOption = 0
            elif a_text_tag['text_tag'] == 'tag':
                textTagOption = 1

            if a_math['math'] == 'counter':
                a_file_select = prompt(q_file_select)
                if a_file_select['file_selection'] == 'file_A' or 'both':
                    countA = spacyTokenTagCounter(df, columnName, textTagOption)
                if a_file_select['file_selection'] == 'file_B' or 'both':
                    countB = spacyTokenTagCounter(df2, columnNameB, textTagOption)

            if a_math['math'] == 'frequency_By_Date':
                a_file_select = prompt(q_file_select)
                a_math_value = prompt(q_math_value)
                value = a_math_value['value']
                if a_file_select['file_selection'] == 'file_A' or 'both':
                    countA = spacyFrequencyByDate(df, columnName, textTagOption, value)
                if a_file_select['file_selection'] == 'file_B' or 'both':
                    countB = spacyFrequencyByDate(df2, columnNameB, textTagOption, value)


def _process_selection_assoc(df, columnName, df2, columnNameB):
    """ :return: df, df2
    function to process the user selections made in the command line user interfaces
        this covers over assocTermAttached() and assocTermDetached() function for the dataframe.
    """
    termStruct = []
    a_assoc = prompt(q_assoc)
    while True:
        print("Term Association:" + str(termStruct))
        a_assoc_method = prompt(q_assoc_method)
        if a_assoc_method['method'] == 'exit':
            break
        if a_assoc_method['method'] == 'insert_term':
            a_assoc_term = prompt(q_assoc_term)
            listIdentity = a_assoc_term['text_tag']
            termInput = a_assoc_term['value']
            termStruct.append([str(termInput), str(listIdentity)])
        if a_assoc_method['method'] == 'run':
            a_file_select = prompt(q_file_select)
            if a_file_select['file_selection'] == 'file_A' or 'both':
                if a_assoc['assoc'] == 'detached':
                    df = assocTermDetached(df, columnName, termStruct)
                if a_assoc['assoc'] == 'attached':
                    df = assocTermAttached(df, columnName, termStruct)
            if a_file_select['file_selection'] == 'file_B' or 'both':
                if a_assoc['assoc'] == 'detached':
                    df2 = assocTermDetached(df2, columnNameB, termStruct)
                if a_assoc['assoc'] == 'attached':
                    df2 = assocTermAttached(df2, columnNameB, termStruct)
    return df, df2


# run
# def _cmd_ui():
while True:
    columnName = columnNameB = defaultColumn()
    a_start = prompt(q_start)
    if a_start['start'] == 'charlyn':
        pass  # charlyn to replace code in this if
    if a_start['start'] == 'guobao':
        pass  # guobao to replace code in this if
    if a_start['start'] == 'nathan':
        pass  # nathan to replace code in this if
    if a_start['start'] == 'gary':
        pass  # gary to replace code in this if

    if a_start['start'] == 'load_file':
        a_file_loc = prompt(q_file_loc)
        df, df2 = _readfile()
        spacyToken(df, columnName)
        # spacyStopword(df, columnName)
        spacyLabelTokenFull(df, columnName)
        spacyToken(df2, columnNameB)
        # spacyStopword(df2, columnNameB)
        spacyLabelTokenFull(df2, columnNameB)

    if a_start['start'] == 'spacy':
        while True:
            a_label = prompt(q_label)
            # pprint(a_label)
            if a_label['venn'] == 'exit':
                break
            if a_label['venn'] == 'display':
                print(df)
                print(df2)
            if a_label['venn'] == 'html':
                a_file_select_html = prompt(q_file_select)
                if a_file_select_html['file_selection'] == 'file_A' or 'both':
                    pass
                if a_file_select_html['file_selection'] == 'file_B' or 'both':
                    pass
            if a_label['venn'] == 'intersect' or a_label['venn'] == 'symmetric_difference' or a_label[
                'venn'] == 'union':
                df, df2 = _process_selection_label(df, columnName, df2, columnNameB)
            if a_label['venn'] == 'modify':
                df, df2 = _process_selection_modify(df, columnName, df2, columnNameB)
            if a_label['venn'] == 'math':
                _process_selection_math(df, columnName, df2, columnNameB)
            if a_label['venn'] == 'term_association':
                df, df2 = _process_selection_assoc(df, columnName, df2, columnNameB)

# print("running cmd ui")
# _cmd_ui()
