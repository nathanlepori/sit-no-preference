# https://pythonprogramming.net/stemming-nltk-tutorial/
import nltk
from nltk.corpus import stopwords

# nltk.download('stopwords')
# from nltk.corpus import treebank # for .draw
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('treebank')#for treebank draw

# sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
sentence = """PRESIDENT gun power life is a kill save help house people world man woman temple church mosque school hate love"""
stop_words = set(stopwords.words('english'))

tokens = nltk.word_tokenize(sentence)
print("==Tokens==")
print(tokens)

print("==Filter out words==")
filtered_sentence = [w for w in tokens if not w in stop_words]
print(filtered_sentence)
# we can use filter to count word frenquncy to find out keywords where its apperance is an indicator of interest.

#dictonary of keywords (volent words, location of interest)???/ more data set will help make a bigger dictionary for analysis
# consider doing named entity group words into categorys such as white house would be organization. Hence a function to search for
# what organization does the individual have interest in.

tagged = nltk.pos_tag(filtered_sentence)
print("==Tagged==")
print(tagged)


from nltk.corpus import wordnet as wn
# nltk.download('wordnet')
print("==Wordnet==")
# print(wn.synsets('vehicle'))
import re
import string
for list in wn.synsets('dog'):
    print(list)
    # SynName = list.strip('Synset(')
    # SynName = list[8:-2]

    print("DEFINITION: " + list.definition())
    print(list.examples())
    print(list.lemmas())
    print([str(lemma.name()) for lemma in list.lemmas()])

# print("==Stanford Tagged==")
# from nltk.tag.stanford import StanfordNERTagger
# nltk.download('stanford-ner/english.all.3class.distsim.crf.ser.gz')
# nltk.download('stanford-ner/stanford-ner.jar')
# st = StanfordNERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz',
#                        'stanford-ner/stanford-ner.jar')
# tags = st.tag(filtered_sentence)
# print(tag)

# print("==Entities==")
# entities = nltk.chunk.ne_chunk(tagged)
# print(entities)
# t = treebank.parsed_sents('wsj_0001.mrg')[0]
# t.draw()

# from nltk.stem import PorterStemmer
# from nltk.tokenize import sent_tokenize, word_tokenize
# ps = PorterStemmer()
# for w in filtered_sentence:
#     print(ps.stem(w))s