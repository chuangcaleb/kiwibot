import pickle

import numpy as np
import mathutils as docbot_mu

########################################
# Load variables
########################################

pickle_data = pickle.load(open("training_data.pickle", "rb"))
vocabulary = pickle_data['vocabulary']
bow = pickle_data['w_bow']
classes = bow.keys()

########################################
# Function Defintions
########################################


def predictAllIntents(query):

    # init
    sim_data = dict.fromkeys(classes)
    vector_query = np.zeros(len(vocabulary))

    # Clean query
    cleaned_query = docbot_mu.clean_query(query)

    # Vectorize query according to our bag of words
    for stem in cleaned_query:
        try:
            index = vocabulary.index(stem)
            vector_query[index] += 1
        except ValueError:
            continue

    # Catch zero-vectors, otherwise scipy.spatial.distance.cosine throws an error
    if not np.any(vector_query):
        zero_data = [(intent, 0) for intent in classes]
        return zero_data

    # Apply term weighting to the vectorized query
    vector_query = docbot_mu.logfreq_weighting(vector_query)

    # Calculate similarity measure against each class
    for intent in classes:
        sim_data[intent] = docbot_mu.sim_cosine(bow[intent], vector_query)
        # print(f'Similarity with {intent}: {sim_data[intent]}')

    # Sort the predicted classes by similarity
    sorted_sim_data = sorted(
        sim_data.items(), key=lambda item: item[1], reverse=True)

    # print(sorted_sim_data)
    return sorted_sim_data


def predictLikeliestIntent(query):
    allIntents = predictAllIntents(query)
    return list(allIntents)[0][0]
