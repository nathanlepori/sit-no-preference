import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
# from nltk.corpus import treebank # for .draw
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('treebank')#for treebank draw

# sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
sentence = """gun power life is a kill house people world man woman """
stop_words = set(stopwords.words('english'))


tokens = nltk.word_tokenize(sentence)
print("==Tokens==")
print(tokens)

print("==Filter out words==")
filtered_sentence = [w for w in tokens if not w in stop_words]
print(filtered_sentence)

tagged = nltk.pos_tag(filtered_sentence)
print("==Tagged==")
print(tagged)

# print("==Entities==")
# entities = nltk.chunk.ne_chunk(tagged)
# print(entities)
# t = treebank.parsed_sents('wsj_0001.mrg')[0]
# t.draw()