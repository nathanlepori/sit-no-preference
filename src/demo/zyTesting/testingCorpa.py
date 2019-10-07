import nltk
from nltk.tokenize import sent_tokenize, PunktSentenceTokenizer
from nltk.corpus import *
nltk.download('gutenberg')
# sample text
sample = gutenberg.raw("bible-kjv.txt")

tok = sent_tokenize(sample)

for x in range(5):
    print(tok[x])