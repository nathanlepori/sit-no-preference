import no_preference.processing.analysis.sort as sort
import pandas as pd

# file = open(r"../words.csv", "r", encoding="utf-8-sig")
# read = Functions1.functionOpenFile("../words.csv")
# read = pd.read_csv("../words.csv",names = ['word','date'])
read = pd.read_csv("../../../dataset/words.csv")
# df['COUNT'] = df.word.str.count('love')

def dfCounter():
    df = pd.DataFrame(read, columns= ['word','date'])

    # df_counter = df.pivot_table(columns=['word'], aggfunc='size')

    df_format = sort.sortBy(df, 'date')
    df_format = sort.sortByDateRange(df_format, 'date', '09/6/2019', '12/6/2019')

    df_counter = df_format.pivot_table(columns=['word'], aggfunc='size')

    print(df_counter)


from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
# filtered_sentence = [w for w in df if not w in stop_words]
# print(filtered_sentence)

# dfCounter()

