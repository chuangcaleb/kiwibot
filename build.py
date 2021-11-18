
# # **HAI Coursework 1: AN INTERACTIVE NLP-BASED AI SYSTEM**
#
# ## Project Title: Chatbot Assistant for Computer Programmers
#
# 20204134 Chuang Caleb hcycc2
#
# BSc Hons Computer Science with Artificial Intelligence
#
# ---
#


# ## **INITIALIZATION**
#
# ### Imports
#

import json
import pickle
from itertools import chain

import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from utils import *

########################################
# ## Loading Intents Data
########################################

data_file = open('intents.json').read()
intents = json.loads(data_file)
tok_doc = {}
classes = []
documents = []
vocabulary = []

########################################
# ## Pre-processing
########################################

# Tokenization and document/class tagging

"""
- tok_doc: class - tokenized phrases
- documents: pattern - its class
- classes: all classes 
"""

for intent in intents['intents']:

    # Tokenize every word
    tok_doc[intent['tag']] = list(chain.from_iterable(
        [nltk.word_tokenize(pattern) for pattern in intent['patterns']]))

    for pattern in intent['patterns']:

        # adding documents
        documents.append((pattern, intent['tag']))

        # adding classes to our class list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

english_stopwords = stopwords.words('english')
ignore_words = [',']
ignore_words.extend(english_stopwords)
lemmatizer = WordNetLemmatizer()

# lemmatize, lowercase and remove stopwords
for intent in classes:
    tok_doc[intent] = [lemmatizer.lemmatize(
        word.lower()) for word in tok_doc[intent] if word not in ignore_words]

# vocabulary: distinct set of all words in documents
vocabulary = sorted(
    list(set(chain.from_iterable([tok_doc[intent] for intent in classes]))))

# sort classes
classes = sorted(list(set(classes)))

print("\n\nDataset statistics:\n")
# documents = combination between patterns and intents
print(len(documents), "documents")
# classes = intents
print(len(classes), "classes", classes)
# words = all words, vocabulary
print(len(vocabulary), "unique lemmatized words", vocabulary)

########################################
# ### Create the bag-of-word model
########################################

# Init vars
training = []
output_empty = [0] * len(classes)

print("\nFirst 10 (alphabetical) words")
print(f'VOCABULARY: {vocabulary[1:10]}\n')

# Fill bag of words
bow = {}
for intent in classes:
    bow[intent] = np.zeros(len(vocabulary))
    for stem in tok_doc[intent]:
        index = vocabulary.index(stem)
        bow[intent][index] += 1
    print(f'{intent}: {bow[intent][1:10]}')


# Weighing function the terms in our bag of words model
for intent in bow:
    bow[intent] = logfreq_weighting(bow[intent])
    # print(f'{intent}: {bow[intent][1:10]}')

########################################
# ### Pickle dump our training data
########################################

pickle.dump({
    'vocabulary': vocabulary,
    'classes': classes,
    'w_bow': bow
},
    open("training_data.pickle", "wb"))
