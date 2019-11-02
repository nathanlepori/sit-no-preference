import nltk
from nltk.corpus import stopwords
import pandas as pd
import no_preference.demo.sort

def readFile(filename):
    read = pd.read_csv(filename)
    return read

def tokenizeColumn(df,columnName):
    df[columnName] = df[columnName].apply(nltk.word_tokenize)
    return df

def filterStopWordColumn(df,columnName):
    stop_words = set(stopwords.words('english'))
    i=0
    for row in df['word']:
        # print(df.iloc[i]['word'])
        df.iloc[i][columnName] = [w for w in df.iloc[i][columnName] if not w in stop_words] #accessing row and remove stop words
        i+=1
    return df

# run this reader
filename = '../../datasets/words.csv'
startDate = '10/06/2019'
endDate= '13/06/2019'
columnName = 'word'

read = readFile(filename)
df = pd.DataFrame(read, columns= ['word','date']) #impt to match columns
df = no_preference.demo.sort.functionSortByDateRange(df, 'date', startDate, endDate)
df = tokenizeColumn(df,columnName)
df = filterStopWordColumn(df,columnName)
print(df)
