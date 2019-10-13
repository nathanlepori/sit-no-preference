# pip install -U spacy
# python -m spacy download en_core_web_sm
#
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
doc = nlp('European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices')
print([(X.text, X.label_ ) for X in doc.ents]) # do not use both
# print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#       token.shape_, token.is_alpha, token.is_stop)
# pos = part of speech
# reference https://spacy.io/api/annotation
print([(X, X.pos_ , X.ent_type_) for X in doc]) # do not use both


# Visualizing dependencies seems to be a good idea to detect complex sentence on SNS.


# # ==================
# import spacy
#
# # Load English tokenizer, tagger, parser, NER and word vectors
# nlp = spacy.load("en_core_web_sm")
#
# # Process whole documents
# text = ("When Sebastian Thrun started working on self-driving cars at "
#         "Google in 2007, few people outside of the company took him "
#         "seriously. “I can tell you very senior CEOs of major American "
#         "car companies would shake my hand and turn away because I wasn’t "
#         "worth talking to,” said Thrun, in an interview with Recode earlier "
#         "this week.")
# doc = nlp(text)
#
# # Analyze syntax
# print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
# print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
#
# # Find named entities, phrases and concepts
# for entity in doc.ents:
#     print(entity.text, entity.label_)