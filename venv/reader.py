import csv

import nltk
from nltk.corpus import stopwords
import pandas as pd
# import wordFrequency
import Functions1


# with open(filename, "r") as f:
#     reader = csv.reader(f, delimiter="\n")
#     for i, line in enumerate(reader):
#         print('line[{}] = {}'.format(i, line))

# with open(filename) as f:
#     line = f.readlines()

# with open(filename, "r") as ins:
#     array = []
#     for line in ins:
#         array.append(line)

def tokenizeColumn(df,columnName):
    df[columnName] = df[columnName].apply(nltk.word_tokenize)
    return df

def readFile(filename):
    read = pd.read_csv(filename)
    return read

def filterStopWordColumn(df,columnName):
    stop_words = set(stopwords.words('english'))
    i=0
    for row in df['word']:
        # print(df.iloc[i]['word'])
        df.iloc[i][columnName] = [w for w in df.iloc[i][columnName] if not w in stop_words] #accessing row and remove stop words
        i+=1
    return df

# run this reader
filename = '..\words.csv'
startDate = '10/06/2019'
endDate= '11/06/2019'
columnName = 'word'

read = readFile(filename)
df = pd.DataFrame(read, columns= ['word','date']) #impt to match columns
df = Functions1.functionSortByDateRange(df,'date',startDate,endDate)
df = tokenizeColumn(df,columnName)
df = filterStopWordColumn(df,columnName)
print(df)
