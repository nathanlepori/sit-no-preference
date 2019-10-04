import nltk
from nltk.corpus import treebank # for .draw
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('treebank')#for treebank draw

sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
tokens = nltk.word_tokenize(sentence)
print("==Tokens==")
print(tokens)
tagged = nltk.pos_tag(tokens)
print("==Tagged==")
print(tagged)
print("==Entities==")
entities = nltk.chunk.ne_chunk(tagged)
print(entities)
t = treebank.parsed_sents('wsj_0001.mrg')[0]
t.draw()