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

def readFiltered(filename):
    wholeData = [];
    with open(filename, 'r') as reader:
        for line in reader:
            # for field in line: #for individual char
            print("======")
            # print(line)
            tokens = nltk.word_tokenize(line)
            # print(tokens)

            # strip stop words
            filtered_sentence = [w for w in tokens if not w in stop_words]
            # print(filtered_sentence)
            # wholeData.append(filtered_sentence)
            # wholeData.extend(filtered_sentence)

            wordFrequency.dfCounter(filtered_sentence, '09/06/2019', '12/06/2019')

    # return wholeData
    # return filtered_sentence

def readDate(filename,startDate,endDate):
    read = pd.read_csv(filename)
    df = pd.DataFrame(read, columns= ['word','date']) #impt to match columns
    df = Functions1.functionSortByDateRange(df,'date',startDate,endDate)
    return df

def filterStopWord(df):
    stop_words = set(stopwords.words('english'))
    # for line in df:
    # for line in df:
    # tokens = df.apply(lambda row: nltk.word_tokenize(row['word']), axis=1)
    df['word'] = df['word'].apply(nltk.word_tokenize)
    # filtered_df = [w for w in tokens['word'] if not w in stop_words]
    # df['word'] = [w for w in df['word'] if not w in stop_words]
    for row in df['word']:
        print("rowVV")
        print(row)
        print("row^^")
        i = 0
        for word in row:
            j = 0
            if word in stop_words:
                print(str(i) + " V|V " + str(j))
                print(df['word'][i][j])
                j+=1
            #     df['word'] = df['word'].replace(word,'')
            #     print(word)
            i+=1
    return df

# run this reader
filename = '..\words.csv'
df = readDate(filename,"10/06/2019","11/06/2019") #restrict to only between dates
# filtered = readFiltered(filename) #filter out stop words
df = filterStopWord(df)
print(df)
