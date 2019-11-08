import json
from os import path

from PyInquirer import prompt
import pandas as pd
from halo import Halo

from no_preference.lib.pyinquirer_menu import data_files_prompt
from no_preference.processing.analysis import venn
from no_preference.processing.analysis.sort import sort_by_date_range
from no_preference.processing.analysis.spacy_nlp import read_file, spacy_token, spacy_label_token_full, \
    spacy_clean_cell, spacy_column_filter_token, spacy_column_strip_token, spacy_token_tag_counter, \
    spacy_frequency_by_date, assoc_term_detached, assoc_term_attached, set_model
from no_preference.processing.analysis.venn import venn_intersect_text_tag, venn_symmetric_dif_text_tag
from no_preference.lib.util import get_data_dir

q_start_analysis = {
    'type': 'rawlist',
    'name': 'start',
    'message': 'Select option >',
    'choices': [
        'load_file',
        'run_analysis',
        'exit',
    ]
}

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

q_set_a_set_b = [
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


def clean_reindex(df_a, column_name_a, df_b, column_name_b):
    if df_a.empty is False:
        df_a = spacy_clean_cell(df_a, column_name_a)
        df_a = df_a.reset_index(drop=True)
    if df_b.empty is False:
        df_b = spacy_clean_cell(df_b, column_name_b)
        df_b = df_b.reset_index(drop=True)
    return df_a, df_b


def write_file_json(content, filename):  # write to file.
    output_datasets_name = path.join(get_data_dir(), 'results', filename)
    with open(output_datasets_name, 'w+') as fp:
        json.dump(content, fp)


def write_file_csv(df, filename):
    output_datasets_name = path.join(get_data_dir(), 'results', filename)
    df.to_csv(output_datasets_name, index=False)


def process_selection_label(df_a, column_name_a, df_b, column_name_b):
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
            text_tag_option = 0
        elif a_text_tag['text_tag'] == 'tag':
            text_tag_option = 1

    with Halo(text=f"Loading intersect function...", spinner='dots'):

        if a_venn['venn'] == 'intersect':
            if df_a.empty is False and df_b.empty is False:
                df_a, df_b = venn_intersect_text_tag(df_a, column_name_a, df_b, column_name_b, text_tag_option)
                df_a, df_b = clean_reindex(df_a, column_name_a, df_b, column_name_b)
            else:
                print("set_A or set_B is empty.")

        if a_venn['venn'] == 'symmetric_difference':
            if df_a.empty is False and df_b.empty is False:
                df_a, df_b = venn_symmetric_dif_text_tag(df_a, column_name_a, df_b, column_name_b, text_tag_option)
                df_a, df_b = clean_reindex(df_a, column_name_a, df_b, column_name_b)
            else:
                print("set_A or set_B is empty.")

        if a_venn['venn'] == 'union':
            if df_a.empty is False and df_b.empty is False:
                df_a = venn.venn_union(df_a, df_b)
                del df_b
                df_b = pd.DataFrame
            else:
                print("set_A or set_B is empty.")

    return df_a, df_b


def process_selection_modify(df_a, column_name_a, df_b, column_name_b, column_date):
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
                text_tag_option = 0
            elif a_text_tag['text_tag'] == 'tag':
                text_tag_option = 1
            a_filter_value = prompt(q_filter_value)
            value = a_filter_value['value']
            a_file_select = prompt(q_file_select)
            with Halo(text=f"Loading modify function...", spinner='dots'):
                if a_filter['modify'] == 'filter':
                    if a_file_select['file_selection'] == 'set_A' or a_file_select[
                        'file_selection'] == 'both' and df_a.empty is False:
                        spacy_column_filter_token(df_a, column_name_a, value, text_tag_option)
                    if a_file_select['file_selection'] == 'set_B' or a_file_select[
                        'file_selection'] == 'both' and df_b.empty is False:
                        spacy_column_filter_token(df_b, column_name_b, value, text_tag_option)

                if a_filter['modify'] == 'strip':
                    if a_file_select['file_selection'] == 'set_A' or a_file_select[
                        'file_selection'] == 'both' and df_a.empty is False:
                        spacy_column_strip_token(df_a, column_name_a, value, text_tag_option)
                    if a_file_select['file_selection'] == 'set_B' or a_file_select[
                        'file_selection'] == 'both' and df_b.empty is False:
                        spacy_column_strip_token(df_b, column_name_b, value, text_tag_option)

        if a_filter['modify'] == 'date':
            a_date = prompt(q_date)
            start_date = a_date['startdate']
            end_date = a_date['enddate']
            a_file_select = prompt(q_file_select)
            with Halo(text=f"Loading modify function...", spinner='dots'):
                if a_file_select['file_selection'] == 'set_A' or a_file_select[
                    'file_selection'] == 'both' and df_a.empty is False:
                    df_a = sort_by_date_range(df_a, column_date, start_date, end_date)
                if a_file_select['file_selection'] == 'set_B' or a_file_select[
                    'file_selection'] == 'both' and df_b.empty is False:
                    df_b = sort_by_date_range(df_b, column_date, start_date, end_date)

        with Halo(text=f"Cleaning up after modify...", spinner='dots'):
            df_a, df_b = clean_reindex(df_a, column_name_a, df_b, column_name_b)

    return df_a, df_b


def process_selection_math(df_a, column_name_a, df_b, column_name_b):
    """ :return: df, df2

    function to process the user selections made in the command line user interfaces
        this covers over the basic mathematical calculation for the dataframe.
            counting by value or counting value by its date
    """
    count_a = []
    count_b = []
    while True:
        a_math = prompt(q_math)
        if a_math['math'] == 'exit':
            break
        if a_math['math'] == 'display':
            if len(count_a) != 0:
                print("set_A:", end=' ')
                print(count_a)
            else:
                print("empty, please run a math method for set_A")
            if len(count_b) != 0:
                print("set_B:", end=' ')
                print(count_b)
            else:
                print("empty, please run a math method for set_B")

        if a_math['math'] == 'save':
            a_file_select = prompt(q_file_select)
            if a_file_select['file_selection'] == 'set_A' or a_file_select['file_selection'] == 'both':
                a_set_A_request = prompt(q_set_A_request)
                filename = a_set_A_request['filename']
                with Halo(text=f"Saving as json.", spinner='dots'):
                    write_file_json(count_a, filename)

            if a_file_select['file_selection'] == 'set_B' or a_file_select['file_selection'] == 'both':
                a_set_B_request = prompt(q_set_B_request)
                filename = a_set_B_request['filename']
                with Halo(text=f"Saving as json.", spinner='dots'):
                    write_file_json(count_b, filename)

        if a_math['math'] == 'counter' or a_math['math'] == 'frequency_By_Date':
            a_text_tag = prompt(q_text_tag)
            if a_text_tag['text_tag'] == 'text':
                text_tag_option = 0
            if a_text_tag['text_tag'] == 'tag':
                text_tag_option = 1

            if a_math['math'] == 'counter':
                a_file_select = prompt(q_file_select)
                with Halo(text=f"Loading counter function...", spinner='dots'):
                    if a_file_select['file_selection'] == 'set_A' or a_file_select['file_selection'] == 'both':
                        if df_a.empty is False:
                            count_a = spacy_token_tag_counter(df_a, column_name_a, text_tag_option)
                        else:
                            print("set_A is empty.")
                    if a_file_select['file_selection'] == 'set_B' or a_file_select['file_selection'] == 'both':
                        if df_b.empty is False:
                            count_b = spacy_token_tag_counter(df_b, column_name_b, text_tag_option)
                        else:
                            print("set_B is empty.")

            if a_math['math'] == 'frequency_By_Date':
                a_file_select = prompt(q_file_select)
                a_math_value = prompt(q_math_value)
                value = a_math_value['value']
                with Halo(text=f"Loading frequency by date function...", spinner='dots'):
                    if a_file_select['file_selection'] == 'set_A' or a_file_select['file_selection'] == 'both':
                        if df_a.empty is False:
                            count_a = spacy_frequency_by_date(df_a, column_name_a, text_tag_option, value)
                        else:
                            print("set_A is empty")
                    if a_file_select['file_selection'] == 'set_B' or a_file_select['file_selection'] == 'both':
                        if df_b.empty is False:
                            count_b = spacy_frequency_by_date(df_b, column_name_b, text_tag_option, value)
                        else:
                            print("set_B is empty")


def _process_selection_assoc(df_a, column_name_a, df_b, column_name_b):
    """ :return: df, df2
    function to process the user selections made in the command line user interfaces
        this covers over assocTermAttached() and assocTermDetached() function for the dataframe.
    """
    term_struct = []
    a_assoc = prompt(q_assoc)
    while True:
        print("Term Association:" + str(term_struct))
        a_assoc_method = prompt(q_assoc_method)
        if a_assoc_method['method'] == 'exit':
            break
        if a_assoc_method['method'] == 'insert_term':
            a_assoc_term = prompt(q_assoc_term)
            list_identity = a_assoc_term['text_tag']
            term_input = a_assoc_term['value']
            term_struct.append([str(term_input), str(list_identity)])
        if a_assoc_method['method'] == 'run':
            a_file_select = prompt(q_file_select)
            with Halo(text=f"Loading term association function...", spinner='dots'):
                if a_file_select['file_selection'] == 'set_A' or a_file_select['file_selection'] == 'both':
                    if df_a.empty is False:
                        if a_assoc['assoc'] == 'detached':
                            df_a = assoc_term_detached(df_a, column_name_a, term_struct)
                        if a_assoc['assoc'] == 'attached':
                            df_a = assoc_term_attached(df_a, column_name_a, term_struct)
                    else:
                        print("set_A is empty.")
                if a_file_select['file_selection'] == 'set_B' or a_file_select['file_selection'] == 'both':
                    if df_b.empty is False:
                        if a_assoc['assoc'] == 'detached':
                            df_b = assoc_term_detached(df_b, column_name_b, term_struct)
                        if a_assoc['assoc'] == 'attached':
                            df_b = assoc_term_attached(df_b, column_name_b, term_struct)
                    else:
                        print("set_B is empty.")
            with Halo(text=f"Cleaning up after term association...", spinner='dots'):
                df_a, df_b = clean_reindex(df_a, column_name_a, df_b, column_name_b)

    return df_a, df_b


def file_loc_generic():
    a_file_loc_generic = data_files_prompt(
        name='file_loc_generic',
        message="What file do you want to use?",
        dir_='datasets',
        allow_custom_file=True,
        custom_file_message="Please indicate the file you want to use?",
        recursive=True
    )
    return a_file_loc_generic


def _process_load_file(df_a, column_name_a, df_b, column_name_b, column_date):
    while True:
        a_set_a_set_b = prompt(q_set_a_set_b)
        if a_set_a_set_b['option'] == 'exit':
            break

        if a_set_a_set_b['option'] == 'set_A':
            a_append_overwrite = prompt(q_append_overwrite)
            # a_file_loc_generic = prompt(q_file_loc_generic)
            a_file_loc_generic = file_loc_generic()
            filename_a = path.join(get_data_dir(), 'datasets', a_file_loc_generic)

            with Halo(text=f"Loading load file function...", spinner='dots'):
                read = read_file(filename_a)
                if a_append_overwrite['integrate'] == 'overwrite' or df_a.empty:
                    # Filter out empty titles (stored as nan aka flat values) and
                    # get only content and date column
                    df_a = read.dropna()[[column_name_a, column_date]]
                    df_a = spacy_token(df_a, column_name_a)
                    df_a = spacy_label_token_full(df_a, column_name_a)
                else:
                    df_temporary = read.dropna()[[column_name_a, column_date]]  # impt to match columns
                    df_temporary = spacy_token(df_temporary, column_name_a)
                    df_temporary = spacy_label_token_full(df_temporary, column_name_a)
                    df_a = venn.venn_union(df_a, df_temporary)

        if a_set_a_set_b['option'] == 'set_B':
            a_append_overwrite = prompt(q_append_overwrite)
            # a_file_loc_generic = prompt(q_file_loc_generic)
            a_file_loc_generic = file_loc_generic()
            filename_b = path.join(get_data_dir(), 'datasets', a_file_loc_generic)

            with Halo(text=f"Loading load file function...", spinner='dots'):
                read = read_file(filename_b)
                if a_append_overwrite['integrate'] == 'overwrite' or df_b.empty:
                    # Filter out empty titles (stored as nan aka flat values) and
                    # get only content and date column
                    df_b = read.dropna()[[column_name_b, column_date]]
                    df_b = spacy_token(df_b, column_name_b)
                    df_b = spacy_label_token_full(df_b, column_name_b)
                else:
                    df_temporary = read.dropna()[[column_name_a, column_date]]  # impt to match columns
                    df_temporary = spacy_token(df_temporary, column_name_b)
                    df_temporary = spacy_label_token_full(df_temporary, column_name_b)
                    df_b = venn.venn_union(df_b, df_temporary)

    return df_a, df_b


def run():
    column_name_a = 'content'
    column_name_b = 'content'
    column_date = 'date'
    df_a = pd.DataFrame
    df_b = pd.DataFrame

    # Let the user pick a model to use
    model = data_files_prompt(
        name='model',
        message="What's the model you want to use for the analysis?",
        dir_='models',
        allow_custom_file=True,
        custom_file_message="What is the name of the model you want to use for the analysis?",
        recursive=False
    )

    set_model(model)
    while True:
        a_start_analysis = prompt(q_start_analysis)
        if a_start_analysis['start'] == 'exit':
            break
        if a_start_analysis['start'] == 'load_file':
            df_a, df_b = _process_load_file(df_a, column_name_a, df_b, column_name_b, column_date)

        if a_start_analysis['start'] == 'run_analysis':
            while True:
                a_label = prompt(q_label)
                if a_label['analysis'] == 'exit':
                    break
                if a_label['analysis'] == 'display':
                    print(df_a)
                    print(df_b)
                if a_label['analysis'] == 'venn':
                    df_a, df_b = process_selection_label(df_a, column_name_a, df_b, column_name_b)
                if a_label['analysis'] == 'modify':
                    df_a, df_b = process_selection_modify(df_a, column_name_a, df_b, column_name_b, column_date)
                if a_label['analysis'] == 'math':
                    process_selection_math(df_a, column_name_a, df_b, column_name_b)
                if a_label['analysis'] == 'term_association':
                    df_a, df_b = _process_selection_assoc(df_a, column_name_a, df_b, column_name_b)
                if a_label['analysis'] == 'save':
                    a_file_select = prompt(q_file_select)
                    if a_file_select['file_selection'] == 'set_A' or a_file_select['file_selection'] == 'both':
                        a_set_a_request = prompt(q_set_A_request)
                        filename = a_set_a_request['filename']
                        with Halo(text=f"Saving as csv...", spinner='dots'):
                            write_file_csv(df_a, filename)
                    if a_file_select['file_selection'] == 'set_B' or a_file_select['file_selection'] == 'both':
                        a_set_b_request = prompt(q_set_B_request)
                        filename = a_set_b_request['filename']
                        with Halo(text=f"Saving as csv...", spinner='dots'):
                            write_file_csv(df_b, filename)


if __name__ == '__main__':
    run()
