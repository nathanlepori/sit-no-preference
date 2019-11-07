import json
from math import isnan
from os import path

from PyInquirer import prompt
import pandas as pd

from no_preference.demo import venn
from no_preference.demo.defaults import defaultFileA, defaultFileB, defaultColumn, defaultDateColumn
from no_preference.demo.sort import sortByDateRange
from no_preference.demo.spacyNLP import readFile, spacyToken, spacyLabelTokenFull, spacyCleanCell, \
    spacyColumnFilterToken, spacyColumnStripToken, spacyTokenTagCounter, spacyFrequencyByDate, assocTermDetached, \
    assocTermAttached, set_model
from no_preference.demo.venn import vennIntersectTextTag, vennSymmetricDifTextTag
from no_preference.util import get_data_dir

# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)
# pd.set_option('display.max_colwidth', 1000)

q_start_analysis = {
    'type': 'rawlist',
    'name': 'start',
    'message': 'Select option >',
    'choices': [
        'load_file',
        'run_analysis',
    ]
}

# q_file_loc = [
#     {
#         'type': 'input',
#         'name': 'set_A',
#         'message': 'Please indicate set_A\'s name and location >',
#     },
#     {
#         'type': 'input',
#         'name': 'set_B',
#         'message': 'Please indicate set_B\'s name and location >',
#     },
# ]

q_file_loc_generic = [
    {
        'type': 'input',
        'name': 'file_loc',
        'message': 'Please indicate the file\'s name and location >',
    },
]

q_label = [
    {
        'type': 'rawlist',
        'name': 'analysis',
        'message': 'Select the functions >',
        'choices': [
            'display',
            'venn',
            'modify',
            'math',
            'term_association',
            'save',
            'exit'
        ]
    },
]
q_venn = [
    {
        'type': 'rawlist',
        'name': 'venn',
        'message': 'Select the type of venn diagram for token with label tag >',
        'choices': [
            'intersect',
            'symmetric_difference',
            'union',
        ]
    }
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

q_file_select = [
    {
        'type': 'rawlist',
        'name': 'file_selection',
        'message': 'Please indicate which set of data to use >',
        'choices': [
            'set_A',
            'set_B',
            'both'
        ]
    },
]

q_filter = [
    {
        'type': 'rawlist',
        'name': 'modify',
        'message': 'Select the type of modification to the Data >',
        'choices': [
            'filter',
            'strip',
            'date',
            'exit'
        ]
    },
]

q_date = [
    {
        'type': 'input',
        'name': 'startdate',
        'message': 'Please input the start date >',
    },
    {
        'type': 'input',
        'name': 'enddate',
        'message': 'Please input the end date >',
    },
]

q_filter_value = [
    {
        'type': 'input',
        'name': 'value',
        'message': 'Please enter value to filter or strip >',
    },
]

q_set_A_request = [
    {
        'type': 'input',
        'name': 'filename',
        'message': 'Please indicate set_A\'s name and location to save content as >',
    }
]

q_set_B_request = [
    {
        'type': 'input',
        'name': 'filename',
        'message': 'Please indicate set_B\'s name and location to save content as >',
    }
]

q_set_A_set_B = [
    {
        'type': 'rawlist',
        'name': 'option',
        'message': 'Select either set_A or set_B, for reading file content into.',
        'choices': [
            'set_A', 'set_B', 'exit'
        ]
    }
]

q_append_overwrite = [  # duplicate
    {
        'type': 'rawlist',
        'name': 'integrate',
        'message': 'Select method of writing to Set',
        'choices': [
            'append',
            'overwrite'
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

q_math_value = [
    {
        'type': 'input',
        'name': 'value',
        'message': 'Please enter value to determine frequency by date >',
    }
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


def cleanReindex(df, columnName, df2, columnNameB):
    if df.empty is False:
        df = spacyCleanCell(df, columnName)
        df = df.reset_index(drop=True)
    if df2.empty is False:
        df2 = spacyCleanCell(df2, columnNameB)
        df2 = df2.reset_index(drop=True)
    return df, df2


def _readfile(name_column, date_column, a_file_loc):
    if a_file_loc['set_A'] == '':
        filenameA = path.join(get_data_dir(), 'datasets', defaultFileA())
    else:
        filenameA = path.join(get_data_dir(), 'datasets', a_file_loc['set_A'])
    read = readFile(filenameA)
    df = pd.DataFrame(read, columns=[name_column, date_column])  # impt to match columns

    if a_file_loc['set_B'] == '':
        filenameB = path.join(get_data_dir(), 'datasets', defaultFileB())
    else:
        filenameB = path.join(get_data_dir(), 'datasets', a_file_loc['set_B'])
    read2 = readFile(filenameB)
    df2 = pd.DataFrame(read2, columns=[name_column, date_column])  # impt to match columns

    return df, df2


def writeFileJson(content, filename):  # write to file.
    output_datasets_name = path.join(get_data_dir(), 'results', filename)
    with open(output_datasets_name, 'w+') as fp:
        json.dump(content, fp)


def writeFileJsonDf(df, filename):  # write to file.
    path_filename = path.join(get_data_dir(), 'datasets', filename)
    df.to_json(path_filename)


def writeFileCsv(df, filename):
    output_datasets_name = path.join(get_data_dir(), 'results', filename)
    df.to_csv(output_datasets_name, index=False)


def _process_selection_label(df, columnName, df2, columnNameB):
    """ :return df, df2:

    function to process the user selections made in the command line user interfaces
        this overs the intersect -> vennIntersectTextTag,
            symmetric difference -> vennSymmetricDifTextTag and
            union -> vennUnion() functions
            from venn.py
    """
    a_venn = prompt(q_venn)
    if a_venn['venn'] == 'intersect' or a_venn['venn'] == 'symmetric_difference':
        a_text_tag = prompt(q_text_tag)  # used to determine which element in a list to use
        if a_text_tag['text_tag'] == 'text':  # eg. to choose either value or text/tage in the list [value,text/tag]
            textTagOption = 0
        elif a_text_tag['text_tag'] == 'tag':
            textTagOption = 1

    if a_venn['venn'] == 'intersect':
        if df.empty is False and df2.empty is False:
            df, df2 = vennIntersectTextTag(df, columnName, df2, columnNameB, textTagOption)
            df, df2 = cleanReindex(df, columnName, df2, columnNameB)
        else:
            print("set_A or set_B is empty.")

    if a_venn['venn'] == 'symmetric_difference':
        if df.empty is False and df2.empty is False:
            df, df2 = vennSymmetricDifTextTag(df, columnName, df2, columnNameB, textTagOption)
            df, df2 = cleanReindex(df, columnName, df2, columnNameB)
        else:
            print("set_A or set_B is empty.")

    if a_venn['venn'] == 'union':
        if df.empty is False and df2.empty is False:
            df = venn.vennUnion(df, df2)
            del df2
            df2 = pd.DataFrame
        else:
            print("set_A or set_B is empty.")

    return df, df2


def _process_selection_modify(df, columnName, df2, columnNameB, date_column):
    """ :return: df, df2

    function to process the user selections made in the command line user interfaces
        this overs the spacyColumnFilterToken() and spacyColumnStripToken() function from spacyNLP.py
    """
    while True:
        a_filter = prompt(q_filter)
        if a_filter['modify'] == 'exit':
            break
        if a_filter['modify'] == 'filter' or a_filter['modify'] == 'strip':
            a_text_tag = prompt(q_text_tag)
            if a_text_tag['text_tag'] == 'text':
                textTagOption = 0
            elif a_text_tag['text_tag'] == 'tag':
                textTagOption = 1
            a_filter_value = prompt(q_filter_value)
            value = a_filter_value['value']
            a_file_select = prompt(q_file_select)
            if a_filter['modify'] == 'filter':
                if a_file_select['file_selection'] == 'set_A' or a_file_select[
                        'file_selection'] == 'both' and df.empty is False:
                    spacyColumnFilterToken(df, columnName, value, textTagOption)
                if a_file_select['file_selection'] == 'set_B' or a_file_select[
                        'file_selection'] == 'both' and df2.empty is False:
                    spacyColumnFilterToken(df2, columnNameB, value, textTagOption)

            if a_filter['modify'] == 'strip':
                if a_file_select['file_selection'] == 'set_A' or a_file_select[
                        'file_selection'] == 'both' and df.empty is False:
                    spacyColumnStripToken(df, columnName, value, textTagOption)
                if a_file_select['file_selection'] == 'set_B' or a_file_select[
                        'file_selection'] == 'both' and df2.empty is False:
                    spacyColumnStripToken(df2, columnNameB, value, textTagOption)

        if a_filter['modify'] == 'date':
            a_date = prompt(q_date)
            start_date = a_date['startdate']
            end_date = a_date['enddate']
            a_file_select = prompt(q_file_select)
            if a_file_select['file_selection'] == 'set_A' or a_file_select[
                    'file_selection'] == 'both' and df.empty is False:
                df = sortByDateRange(df, date_column, start_date, end_date)
            if a_file_select['file_selection'] == 'set_B' or a_file_select[
                    'file_selection'] == 'both' and df2.empty is False:
                df2 = sortByDateRange(df2, date_column, start_date, end_date)

        df, df2 = cleanReindex(df, columnName, df2, columnNameB)

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
                print("set_A:", end=' ')
                print(countA)
            else:
                print("empty, please run a math method for set_A")
            if len(countB) != 0:
                print("set_B:", end=' ')
                print(countB)
            else:
                print("empty, please run a math method for set_B")

        if a_math['math'] == 'save':
            a_file_select = prompt(q_file_select)
            if a_file_select['file_selection'] == 'set_A' or a_file_select['file_selection'] == 'both':
                a_set_A_request = prompt(q_set_A_request)
                filename = a_set_A_request['filename']
                writeFileJson(countA, filename)

            if a_file_select['file_selection'] == 'set_B' or a_file_select['file_selection'] == 'both':
                a_set_B_request = prompt(q_set_B_request)
                filename = a_set_B_request['filename']
                writeFileJson(countB, filename)

        if a_math['math'] == 'counter' or a_math['math'] == 'frequency_By_Date':
            a_text_tag = prompt(q_text_tag)
            if a_text_tag['text_tag'] == 'text':
                textTagOption = 0
            if a_text_tag['text_tag'] == 'tag':
                textTagOption = 1

            if a_math['math'] == 'counter':
                a_file_select = prompt(q_file_select)
                if a_file_select['file_selection'] == 'set_A' or a_file_select['file_selection'] == 'both':
                    if df.empty is False:
                        countA = spacyTokenTagCounter(df, columnName, textTagOption)
                    else:
                        print("set_A is empty.")
                if a_file_select['file_selection'] == 'set_B' or a_file_select['file_selection'] == 'both':
                    if df2.empty is False:
                        countB = spacyTokenTagCounter(df2, columnNameB, textTagOption)
                    else:
                        print("set_B is empty.")

            if a_math['math'] == 'frequency_By_Date':
                a_file_select = prompt(q_file_select)
                a_math_value = prompt(q_math_value)
                value = a_math_value['value']
                if a_file_select['file_selection'] == 'set_A' or a_file_select['file_selection'] == 'both':
                    if df.empty is False:
                        countA = spacyFrequencyByDate(df, columnName, textTagOption, value)
                    else:
                        print("set_A is empty")
                if a_file_select['file_selection'] == 'set_B' or a_file_select['file_selection'] == 'both':
                    if df2.empty is False:
                        countB = spacyFrequencyByDate(df2, columnNameB, textTagOption, value)
                    else:
                        print("set_B is empty")


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
            if a_file_select['file_selection'] == 'set_A' or a_file_select['file_selection'] == 'both':
                if df.empty is False:
                    if a_assoc['assoc'] == 'detached':
                        df = assocTermDetached(df, columnName, termStruct)
                    if a_assoc['assoc'] == 'attached':
                        df = assocTermAttached(df, columnName, termStruct)
                else:
                    print("set_A is empty.")
            if a_file_select['file_selection'] == 'set_B' or a_file_select['file_selection'] == 'both':
                if df2.empty is False:
                    if a_assoc['assoc'] == 'detached':
                        df2 = assocTermDetached(df2, columnNameB, termStruct)
                    if a_assoc['assoc'] == 'attached':
                        df2 = assocTermAttached(df2, columnNameB, termStruct)
                else:
                    print("set_B is empty.")

            df, df2 = cleanReindex(df, columnName, df2, columnNameB)

    return df, df2


def _process_load_file(df, columnName, df2, columnNameB, date_column):
    while True:
        a_set_A_set_B = prompt(q_set_A_set_B)
        if a_set_A_set_B['option'] == 'exit':
            break

        if a_set_A_set_B['option'] == 'set_A':
            a_append_overwrite = prompt(q_append_overwrite)
            a_file_loc_generic = prompt(q_file_loc_generic)
            if a_file_loc_generic['file_loc'] == '':
                output_datasets_name = path.join(get_data_dir(), 'datasets', defaultFileA())
                filenameA = output_datasets_name
            else:
                filenameA = path.join(get_data_dir(), 'datasets', a_file_loc_generic['file_loc'])

            read = readFile(filenameA)
            if a_append_overwrite['integrate'] == 'overwrite' or df.empty:
                # Filter out empty titles (stored as nan aka flat values) and
                # get only content and date column
                df = read.dropna()[[columnName, date_column]]
                df = spacyToken(df, columnName)
                df = spacyLabelTokenFull(df, columnName)
            else:
                df_temporary = read.dropna()[[columnName, date_column]]  # impt to match columns
                df_temporary = spacyToken(df_temporary, columnName)
                df_temporary = spacyLabelTokenFull(df_temporary, columnName)
                df = venn.vennUnion(df, df_temporary)

        if a_set_A_set_B['option'] == 'set_B':
            a_append_overwrite = prompt(q_append_overwrite)
            a_file_loc_generic = prompt(q_file_loc_generic)
            if a_file_loc_generic['file_loc'] == '':
                output_datasets_name = path.join(get_data_dir(), 'datasets', defaultFileB())
                filenameB = output_datasets_name
            else:
                filenameB = path.join(get_data_dir(), 'datasets', a_file_loc_generic['file_loc'])

            read = readFile(filenameB)
            if a_append_overwrite['integrate'] == 'overwrite' or df2.empty:
                # Filter out empty titles (stored as nan aka flat values) and
                # get only content and date column
                df2 = read.dropna()[[columnName, date_column]]
                df2 = spacyToken(df2, columnName)
                df2 = spacyLabelTokenFull(df2, columnName)
            else:
                df_temporary = read.dropna()[[columnName, date_column]]  # impt to match columns
                df_temporary = spacyToken(df_temporary, columnNameB)
                df_temporary = spacyLabelTokenFull(df_temporary, columnNameB)
                df2 = venn.vennUnion(df2, df_temporary)

    return df, df2


def run():
    columnName = columnNameB = defaultColumn()
    date_column = defaultDateColumn()
    df = pd.DataFrame
    df2 = pd.DataFrame

    # Let the user pick a model to use
    a_model = prompt({
        'type': 'input',
        'name': 'model',
        'message': "What's the name of the model you want to use for the analysis?",
        'validate': 'required'
    })
    set_model(a_model['model'])
    while True:
        a_start_analysis = prompt(q_start_analysis)
        if a_start_analysis['start'] == 'load_file':
            df, df2 = _process_load_file(df, columnName, df2, columnNameB, date_column)

        if a_start_analysis['start'] == 'run_analysis':
            while True:
                a_label = prompt(q_label)
                if a_label['analysis'] == 'exit':
                    break
                if a_label['analysis'] == 'display':
                    print(df)
                    print(df2)
                if a_label['analysis'] == 'venn':
                    df, df2 = _process_selection_label(df, columnName, df2, columnNameB)
                if a_label['analysis'] == 'modify':
                    df, df2 = _process_selection_modify(df, columnName, df2, columnNameB, date_column)
                if a_label['analysis'] == 'math':
                    _process_selection_math(df, columnName, df2, columnNameB)
                if a_label['analysis'] == 'term_association':
                    df, df2 = _process_selection_assoc(df, columnName, df2, columnNameB)
                if a_label['analysis'] == 'save':
                    a_file_select = prompt(q_file_select)
                    if a_file_select['file_selection'] == 'set_A' or a_file_select['file_selection'] == 'both':
                        a_set_A_request = prompt(q_set_A_request)
                        filename = a_set_A_request['filename']
                        writeFileCsv(df, filename)
                        # writeFileJsonDf(df, filename)
                    if a_file_select['file_selection'] == 'set_B' or a_file_select['file_selection'] == 'both':
                        a_set_B_request = prompt(q_set_B_request)
                        filename = a_set_B_request['filename']
                        writeFileCsv(df2, filename)
                        # writeFileJsonDf(df2, filename)


if __name__ == '__main__':
    run()
