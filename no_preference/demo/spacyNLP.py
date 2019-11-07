import pandas as pd
import spacy
from pandas import DataFrame
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.language import Language

import datetime
import no_preference.demo.venn as venn
import no_preference.demo.sort as sort
import no_preference.demo.defaults as defaults
from no_preference.util import load_model

nlp: Language


def set_model(name: str):
    global nlp
    nlp = load_model(name)


def readFile(filename):
    read = pd.read_csv(filename)
    return read


def tokenize_cell(cell: str):
    doc = nlp(cell)
    return [w.lemma_ for w in doc]


def spacyToken(df: DataFrame, columnName):
    """ change content of columnName into token """
    df[columnName] = df[columnName].apply(tokenize_cell)
    return df


def spacyStopword(df, columnName):
    """must have been tokenized"""
    i = 0
    for row in df[columnName]:
        for word in df.iloc[i][columnName]:
            df.iloc[i][columnName] = [w for w in df.iloc[i][columnName] if nlp.vocab[w].is_stop == False]
        i += 1
    return df


def spacyLabel(df, columnName):
    """ change content of columnName into token together with a label.
    The label will be made for words that can be identified as Location, Person, Date, Money etc.
    If it cannot be identified it will be discarded.  """
    i = 0
    for row in df[columnName]:
        doc = nlp(df.iloc[i][columnName])
        df.iloc[i][columnName] = [[X.text, X.label_] for X in doc.ents]
        i += 1
    return df


def spacyLabelToken(df, columnName):  # same as spacyLabel but refix exisiting tokens
    """ Same as spacyLabel however the dataframe content of columnName have already been tokenized.
    As spacyLabel will not be able to provide labels on tokenized content.  """
    i = 0
    for row in df[columnName]:
        format_token = ' '.join(map(str, row))
        doc = nlp(format_token)
        df.iloc[i][columnName] = [[X.text, X.label_] for X in doc.ents]
        i += 1
    return df


def spacyLabelTokenFull(df, columnName):  # same as spacyLabel but refix exisiting tokens
    """ Same as spacyLabel however the dataframe content of columnName have already been tokenized.
    As spacyLabel will not be able to provide labels on tokenized content.  """
    i = 0
    for row in df[columnName]:
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

        df.iloc[i][columnName] = full
        i += 1
    return df


def spacyPOS(df, columnName):
    """ change content of columnName into token together with a Part-Of-Speech.
    each words will be identified for its Part-Of-Speech such as NOUN, Adjectives.
    This Part-of-Speech will be attached to each word together to form a list. """
    i = 0
    for row in df[columnName]:
        doc = nlp(df.iloc[i][columnName])
        df.iloc[i][columnName] = [[X.text, X.pos_] for X in doc]
        i += 1
    return df


def spacyPOSToken(df, columnName):
    """ Same as spacyPOS however the dataframe content of columnName have already been tokenized.
    As spacyPOS will not be able to provide Part-Of-Speech on tokenized content. """
    i = 0
    for row in df[columnName]:
        format_token = ' '.join(map(str, row))
        doc = nlp(format_token)
        df.iloc[i][columnName] = [[X.text, X.pos_] for X in doc]
        i += 1
    return df


def spacyColumnFilterToken(df, columnName, value, listNo):  # remove any that match value
    """ The precondition to using this function is to have the columnName to have been process
    with either spacyLabel or spacyPOS.
    This function will remove all words that does not match the variable value
    (while ignoring content of spacyLabel or spacyPOS)
    listNo is used to select either the text/token itself or the POS/label"""
    i = 0
    for row in df[columnName]:
        j = 0
        for word in df.iloc[i][columnName]:
            df.iloc[i][columnName][j] = [w for w in df.iloc[i][columnName][j] if
                                         df.iloc[i][columnName][j][listNo] == value]
            j += 1
        i += 1
    return df


def spacyColumnStripToken(df, columnName, value, listNo):  # remove all that is not value
    """ The precondition to using this function is to have the columnName to have been process
    with either spacyLabel or spacyPOS.
    This function will remove all words that does match the variable value
    (while ignoring content of spacyLabel or spacyPOS) """
    for row in df[columnName]:
        for word in row:
            word[:] = [w for w in word[:] if word[:][listNo] != value]  # one is !=
    return df


def spacyCleanCell(df, columnName):
    """ After working with some other functions,
    there might be cells in columnName that contains empty list.
    This function is to clean up such list"""
    df = sort.reindex(df)
    i = 0
    # for row in df[columnName]:
    totalRow = len(df[columnName])
    while i < totalRow:
        for word in df[columnName].loc[i]:
            df[columnName].loc[i] = [x for x in df[columnName].loc[i] if x]
        if len(df[columnName].loc[i]) == 0:  # double check if work
            df.drop(i, inplace=True)
        i += 1
    return df


def spacyCleanRow(df, columnName):
    i = 0
    totalRow = len(df[columnName])
    while i < totalRow:
        if len(df[columnName].loc[i]) == 0:  # double check if work
            df.drop(i, inplace=True)
        i += 1
    return df


def spacyTokenTagCounter(df, columnName, listNo):
    i = 0
    counter = dict()
    for row in df[columnName]:
        for word in df.iloc[i][columnName]:
            counter[word[listNo]] = counter.get(word[listNo], 0) + 1
        i += 1
    return counter


def spacyFrequencyByDate(df, columnName, listNo, value):
    i = 0
    counter = dict()
    for row in df[columnName]:
        for word in df.iloc[i][columnName]:
            if word[listNo] == value:
                temp = datetime.datetime.strptime(df.iloc[i][defaults.defaultDateColumn()],'%Y-%m-%d %H:%M:%S').date()
                concat = temp.strftime("%Y-%m-%d")
                counter[concat] = counter.get(concat, 0) + 1
        i += 1
    return counter


def assocTermDetached(df, columnName, termStruct):
    """
    a filter function to keep only rows in dataframe where it must contains all elements within termStruct,
        in no particular sequence.
    termStruct refers to the user input of which results in a list [value, text or tag]
    """
    i = 0
    for row in df[columnName]:
        tempStruct = termStruct.copy()
        for word in df.iloc[i][columnName]:
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
            df.iloc[i][columnName] = []
        i += 1
    return df


def assocTermAttached(df, columnName, termStruct):
    """
       a filter function to keep only rows in dataframe where it must contains all elements within termStruct,
           in sequence of the list termStruct.
       termStruct refers to the user input of which results in a list
            eg. [ [1st value, text or tag] , [2nd value, text or tag] ]
       """
    df = sort.reindex(df)
    i = 0
    for row in df[columnName]:
        termLength = len(termStruct)
        t = 0
        for word in df.iloc[i][columnName]:
            if t >= termLength:  # when correct number of matches
                break
            if termStruct[t][1] == 'text':
                listNo = 0
            else:
                listNo = 1
            if termStruct[t][0] in word[listNo]:  # if value match remove from list of struct to track
                t += 1
            else:
                t = 0  # if failed to match start again for tempStruct
        if t != termLength:
            df.iloc[i][columnName] = []
        i += 1
    return df
