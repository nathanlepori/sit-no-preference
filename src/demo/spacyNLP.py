import pandas as pd
import spacy
import src.demo.venn
nlp = spacy.load("en_core_web_sm")


def readFile(filename):
    read = pd.read_csv(filename)
    return read

def spacyToken(df, columnName):
    i = 0
    for row in df[columnName]:
        doc = nlp(df.iloc[i][columnName])
        df.iloc[i][columnName] = ([w.text for w in doc])
        # print(df.iloc[i][columnName])
        i += 1
    return df

def spacyLabel(df, columnName):
    i = 0
    for row in df[columnName]:
        doc = nlp(df.iloc[i][columnName])
        df.iloc[i][columnName] = [(X.text, X.label_) for X in doc.ents]
        i += 1
    return df

def spacyLabelToken(df, columnName): #same as spacyLabel but refix exisiting tokens
    i = 0
    for row in df[columnName]:
        format_token = ' '.join(map(str, row))
        doc = nlp(format_token)
        df.iloc[i][columnName] = [(X.text, X.label_) for X in doc.ents]
        i += 1
    return df

def spacyPOSToken(df, columnName):  #same as spacyPOS but refix exisiting tokens
    i = 0
    for row in df[columnName]:
        format_token = ' '.join(map(str, row))
        doc = nlp(format_token)
        df.iloc[i][columnName] = [[X.text, X.pos_] for X in doc]
        i += 1
    return df

def spacyPOS(df, columnName):
    i = 0
    for row in df[columnName]:
        doc = nlp(df.iloc[i][columnName])
        df.iloc[i][columnName] = [[X.text, X.pos_] for X in doc]
        i += 1
    return df

def spacyColumnFilterToken(df, columnName, value, listNo):  # remove any that match value
    #must use with either label or pos
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
    #must use with either label or pos
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
src.demo.venn.vennIntersect(df,columnName,df2,columnName)
# # src.demo.venn.vennUniqueSymmetricDif(df,columnName,df2,columnName)
# src.demo.venn.vennSymmetricDif(df,columnName,df2,columnName)
# #required group tgt 2

# df = spacyColumnStripToken(df, columnName, 'love', 0)



# df = spacyPOSToken(df, columnName)
# df2 = spacyPOSToken(df2, columnName)

df = spacyCleanCell(df,columnName)
df2 = spacyCleanCell(df2,columnName)
print(df)
print(df2)