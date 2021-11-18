import pickle

import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from mathutils import *

########################################
# Prediction function
########################################


data = pickle.load(open("training_data.pickle", "rb"))
vocabulary = data['vocabulary']
classes = data['classes']
bow = data['w_bow']

lemmatizer = WordNetLemmatizer()


def predictAllIntents(query):

    # init
    sim_data = dict.fromkeys(classes)
    vector_query = np.zeros(len(vocabulary))

    # tokenize query
    tok_query = nltk.word_tokenize(query)

    # Remove stopwords, lowercase
    english_stopwords = stopwords.words('english')
    filtered_query = [word.lower() for word in tok_query
                      if word.lower() not in english_stopwords]

    # Stemming --> Lemmatising
    stemmed_query = [lemmatizer.lemmatize(word) for word in filtered_query]

    # Vectorize query according to our bag of words
    for stem in stemmed_query:
        try:
            index = vocabulary.index(stem)
            vector_query[index] += 1
        except ValueError:
            continue

    # Apply term weighing to the vectorized query
    vector_query = logfreq_weighting(vector_query)

    # Calculate similarity measure against each class
    for intent in bow.keys():
        sim_data[intent] = sim_cosine(bow[intent], vector_query)
        print(f'Similarity with {intent}: {sim_data[intent]}')

    # Sort the predicted classes by similarity
    sorted_sim_data = sorted(
        sim_data.items(), key=lambda item: item[1], reverse=True)

    return sorted_sim_data


def predictLikeliestIntent(query):
    allIntents = predictAllIntents(query)
    return list(allIntents)[1][0]
