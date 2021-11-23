
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

# ### Imports

import json
import pickle
from itertools import chain

import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from docbot import mathutils as docbot_mu

########################################
# ## Loading Intents Data
########################################

data_file = open('intents.json').read()
intents_file = json.loads(data_file)

tok_doc = {}
intents = {}
classes = []
vocabulary = []

########################################
# ## Pre-processing
########################################

for intent in intents_file['intents']:

    # Only if intent has a pattern, then add it as a class for the classifier
    if 'patterns' in intent:
        # Load every pattern in every intent
        intents[intent['tag']] = [pattern for pattern in intent['patterns']]
        classes.append(intent['tag'])

# lemmatize, lowercase and remove stopwords
for intent in intents:
    tok_doc[intent] = list(chain.from_iterable(docbot_mu.clean_query(
        pattern) for pattern in intents[intent]))
    # tok_doc[intent] = [clean_query(word) for word in tok_doc[intent]]

# vocabulary: distinct set of all words in documents
vocabulary = sorted(
    list(set(chain.from_iterable([tok_doc[intent] for intent in classes]))))

# sort classes
classes = sorted(list(set(classes)))

print("\n\nDataset statistics:\n")
# classes = intents
# ? print(len(classes), "classes", classes)
# words = all words, vocabulary
# ? print(len(vocabulary), "unique lemmatized words", vocabulary)

########################################
# ### Create the bag-of-word model
########################################

# Init vars
training = []
output_empty = [0] * len(classes)

print("\nFirst 10 (alphabetical) words")
print(f'VOCABULARY: {vocabulary[1:10]}')

# Fill bag of words
bow = {}
print("\nVectors of first 10 words")
for intent in classes:
    bow[intent] = np.zeros(len(vocabulary))
    for stem in tok_doc[intent]:
        index = vocabulary.index(stem)
        bow[intent][index] += 1
    print(f'{intent}: {bow[intent][1:10]}')


# Weighting function for the terms in our bag of words model
for intent in bow:
    bow[intent] = docbot_mu.logfreq_weighting(bow[intent])
    # print(f'{intent}: {bow[intent][1:10]}')

########################################
# ### Pickle dump our training data
########################################

pickle.dump({
    'vocabulary': vocabulary,
    'classes': classes,
    'w_bow': bow},
    open("training_data.pickle", "wb"))
