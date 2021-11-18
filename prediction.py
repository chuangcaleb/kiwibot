import pickle

import numpy as np
import mathutils as docbot_mu

########################################
# Load variables
########################################

pickle_data = pickle.load(open("training_data.pickle", "rb"))
vocabulary = pickle_data['vocabulary']
classes = pickle_data['classes']
bow = pickle_data['w_bow']


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

    # Apply term weighing to the vectorized query
    vector_query = docbot_mu.logfreq_weighting(vector_query)

    # Calculate similarity measure against each class
    for intent in bow.keys():
        sim_data[intent] = docbot_mu.sim_cosine(bow[intent], vector_query)
        print(f'Similarity with {intent}: {sim_data[intent]}')

    # Sort the predicted classes by similarity
    sorted_sim_data = sorted(
        sim_data.items(), key=lambda item: item[1], reverse=True)

    return sorted_sim_data


def predictLikeliestIntent(query):
    allIntents = predictAllIntents(query)
    return list(allIntents)[0][0]
