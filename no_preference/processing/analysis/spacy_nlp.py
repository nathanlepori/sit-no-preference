import pandas as pd
from pandas import DataFrame
from spacy.language import Language

import datetime
import no_preference.processing.analysis.sort as sort
from no_preference.lib.util import load_model

nlp: Language


def set_model(name: str):
    global nlp
    nlp = load_model(name)


def read_file(filename):
    read = pd.read_csv(filename)
    return read


def tokenize_cell(cell: str):
    doc = nlp(cell)
    return [w.lemma_ for w in doc]


def spacy_token(df: DataFrame, column_name):
    """ change content of columnName into token """
    df[column_name] = df[column_name].apply(tokenize_cell)
    return df


def spacy_stop_word(df, column_name):
    """must have been tokenized"""
    i = 0
    for row in df[column_name]:
        for word in df.iloc[i][column_name]:
            df.iloc[i][column_name] = [w for w in df.iloc[i][column_name] if nlp.vocab[w].is_stop == False]
        i += 1
    return df


def spacy_label_token_full(df, column_name):  # same as spacyLabel but refix exisiting tokens
    """ Same as spacyLabel however the dataframe content of columnName have already been tokenized.
    As spacyLabel will not be able to provide labels on tokenized content.  """
    i = 0
    for row in df[column_name]:
        format_token = ' '.join(map(str, row))
        doc = nlp(format_token)
        # for ent in doc.ents:
        #     print(ent.text, ent.label_)
        modify = format_token
        full = []
        for de in doc.ents:
            entpos = modify.find(de.text)
            extract = modify[:entpos]
            extractToken = list(extract.split(' '))
            for et in extractToken:
                if len(et) != 0:
                    full.append([et, 'x'])
            full.append([de.text, de.label_])
            modify = modify[entpos + len(de.text):]
        # print("toooken>> "+str(modify)+" "+str(len(modify)))
        if len(modify) != 0:
            extractToken = list(modify.split(' '))
            for leftover in extractToken:
                if len(leftover) != 0:
                    full.append([leftover, 'x'])

        df.iloc[i][column_name] = full
        i += 1
    return df


def spacy_column_filter_token(df, column_name, value, list_no):  # remove any that match value
    """ The precondition to using this function is to have the columnName to have been process
    with either spacyLabel or spacyPOS.
    This function will remove all words that does not match the variable value
    (while ignoring content of spacyLabel or spacyPOS)
    listNo is used to select either the text/token itself or the POS/label"""
    i = 0
    for row in df[column_name]:
        j = 0
        for word in df.iloc[i][column_name]:
            df.iloc[i][column_name][j] = [w for w in df.iloc[i][column_name][j] if
                                          df.iloc[i][column_name][j][list_no] == value]
            j += 1
        i += 1
    return df


def spacy_column_strip_token(df, column_name, value, list_no):  # remove all that is not value
    """ The precondition to using this function is to have the columnName to have been process
    with either spacyLabel or spacyPOS.
    This function will remove all words that does match the variable value
    (while ignoring content of spacyLabel or spacyPOS) """
    for row in df[column_name]:
        for word in row:
            word[:] = [w for w in word[:] if word[:][list_no] != value]  # one is !=
    return df


def spacy_clean_cell(df, column_name):
    """ After working with some other functions,
    there might be cells in columnName that contains empty list.
    This function is to clean up such list"""
    df = sort.reindex(df)
    i = 0
    # for row in df[columnName]:
    total_row = len(df[column_name])
    while i < total_row:
        for word in df[column_name].loc[i]:
            df[column_name].loc[i] = [x for x in df[column_name].loc[i] if x]
        if len(df[column_name].loc[i]) == 0:  # double check if work
            df.drop(i, inplace=True)
        i += 1
    return df


def spacy_token_tag_counter(df, column_name, list_no):
    i = 0
    counter = dict()
    for row in df[column_name]:
        for word in df.iloc[i][column_name]:
            counter[word[list_no]] = counter.get(word[list_no], 0) + 1
        i += 1
    return counter


def spacy_frequency_by_date(df, column_name, list_no, value):
    i = 0
    counter = dict()
    for row in df[column_name]:
        for word in df.iloc[i][column_name]:
            if word[list_no] == value:
                temp = datetime.datetime.strptime(df.iloc[i]['date'],'%Y-%m-%d %H:%M:%S').date()
                concat = temp.strftime("%Y-%m-%d")
                counter[concat] = counter.get(concat, 0) + 1
        i += 1
    return counter


def assoc_term_detached(df, column_name, term_struct):
    """
    a filter function to keep only rows in dataframe where it must contains all elements within termStruct,
        in no particular sequence.
    termStruct refers to the user input of which results in a list [value, text or tag]
    """
    i = 0
    for row in df[column_name]:
        tempStruct = term_struct.copy()
        for word in df.iloc[i][column_name]:
            t = 0
            for element in tempStruct:
                if tempStruct[t][1] == 'text':
                    listNo = 0
                else:
                    listNo = 1
                if word[listNo] == tempStruct[t][0]:  # if value match remove from list of struct to track
                    del tempStruct[t]
                t += 1
        if len(tempStruct) > 0:
            df.iloc[i][column_name] = []
        i += 1
    return df


def assoc_term_attached(df, column_name, term_struct):
    """
       a filter function to keep only rows in dataframe where it must contains all elements within termStruct,
           in sequence of the list termStruct.
       termStruct refers to the user input of which results in a list
            eg. [ [1st value, text or tag] , [2nd value, text or tag] ]
       """
    df = sort.reindex(df)
    i = 0
    for row in df[column_name]:
        term_length = len(term_struct)
        t = 0
        for word in df.iloc[i][column_name]:
            if t >= term_length:  # when correct number of matches
                break
            if term_struct[t][1] == 'text':
                list_no = 0
            else:
                list_no = 1
            if term_struct[t][0] in word[list_no]:  # if value match remove from list of struct to track
                t += 1
            else:
                t = 0  # if failed to match start again for tempStruct
        if t != term_length:
            df.iloc[i][column_name] = []
        i += 1
    return df
