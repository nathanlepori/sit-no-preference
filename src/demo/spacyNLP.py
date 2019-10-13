import pandas as pd
import spacy
import src.demo.venn as venn
import src.demo.sort as sort
nlp = spacy.load("en_core_web_sm")


def readFile(filename):
    read = pd.read_csv(filename)
    return read

def spacyToken(df, columnName):
    """ change content of columnName into token """
    i = 0
    for row in df[columnName]:
        doc = nlp(df.iloc[i][columnName])
        df.iloc[i][columnName] = ([w.text for w in doc])
        # print(df.iloc[i][columnName])
        i += 1
    return df

def spacyLabel(df, columnName):
    """ change content of columnName into token together with a label.
    The label will be made for words that can be identified as Location, Person, Date, Money etc.
    If it cannot be identified it will be discarded.  """
    i = 0
    for row in df[columnName]:
        doc = nlp(df.iloc[i][columnName])
        df.iloc[i][columnName] = [(X.text, X.label_) for X in doc.ents]
        i += 1
    return df

def spacyLabelToken(df, columnName): #same as spacyLabel but refix exisiting tokens
    """ Same as spacyLabel however the dataframe content of columnName have already been tokenized.
    As spacyLabel will not be able to provide labels on tokenized content.  """
    i = 0
    for row in df[columnName]:
        format_token = ' '.join(map(str, row))
        doc = nlp(format_token)
        df.iloc[i][columnName] = [(X.text, X.label_) for X in doc.ents]
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
    (while ignoring content of spacyLabel or spacyPOS) """
    i = 0
    for row in df[columnName]:
        j = 0
        for word in df.iloc[i][columnName]:
            df.iloc[i][columnName][j] = [w for w in df.iloc[i][columnName][j] if df.iloc[i][columnName][j][listNo] == value]
            # print(df.iloc[i][columnName][j])
            j += 1
        i += 1
    return df

def spacyColumnStripToken(df, columnName, value, listNo):  # remove all that is not value
    """ The precondition to using this function is to have the columnName to have been process
    with either spacyLabel or spacyPOS.
    This function will remove all words that does match the variable value
    (while ignoring content of spacyLabel or spacyPOS) """
    i = 0
    for row in df[columnName]:
        j = 0
        for word in df.iloc[i][columnName]:
            df.iloc[i][columnName][j] = [w for w in df.iloc[i][columnName][j] if
                                         df.iloc[i][columnName][j][listNo] != value]  # one is !=
            # print(df.iloc[i][columnName][j])
            j += 1
        i += 1
    return df

def spacyCleanCell(df,columnName):
    """ After working with some other functions,
    there might be cells in columnName that contains empty list.
    This function is to clean up such list"""
    i = 0
    for row in df[columnName]:
        for word in df.iloc[i][columnName]:
            df.iloc[i][columnName] = [x for x in df.iloc[i][columnName] if x]
        i += 1
    return df

# run this reader
filename = '..\..\dataset\words.csv'
filename2 = '..\..\dataset\words2.csv'
startDate = '10/06/2019'
endDate = '13/06/2019'
columnName = 'word'
#
read = readFile(filename)
df = pd.DataFrame(read, columns=['word', 'date'])  # impt to match columns
read2 = readFile(filename2)
df2 = pd.DataFrame(read2, columns=['word', 'date'])  # impt to match columns

# df = spacyLabel(df, columnName)
# df2 = spacyLabel(df2, columnName)


df = spacyToken(df,columnName)
df2 = spacyToken(df2,columnName)

# df = spacyPOS(df, columnName)
# df2 = spacyPOS(df2, columnName)

# print(df)
# print(df2)
#
# df = spacyPOSToken(df, columnName)
# df2 = spacyPOSToken(df2, columnName)

# df = spacyColumnStripToken(df, columnName, 'love', 0)
# df2 = spacyColumnFilterToken(df2, columnName, 'love', 0)



# #required group tgt 2
# df = spacyToken(df,columnName)
# df2 = spacyToken(df2,columnName)
# # src.demo.venn.vennUniqueIntersect(df,columnName,df2,columnName)
# src.demo.venn.vennIntersect(df,columnName,df2,columnName)
# # src.demo.venn.vennUniqueSymmetricDif(df,columnName,df2,columnName)
# src.demo.venn.vennSymmetricDif(df,columnName,df2,columnName)
# #required group tgt 2

# df = spacyColumnStripToken(df, columnName, 'love', 0)



# df = spacyPOSToken(df, columnName)
# df2 = spacyPOSToken(df2, columnName)

# df = spacyCleanCell(df,columnName)
# df2 = spacyCleanCell(df2,columnName)
#
# print(df)
# print(df2)

union_df = venn.vennUnion(df,df2)
# union_df = sort.functionSortBy(union_df,'date')
# union_df = sort.reindex(union_df)
print(union_df)