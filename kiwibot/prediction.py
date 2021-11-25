import pickle

import numpy as np
from kiwibot import mathutils as kiwibot_mu

########################################
# Load variables
########################################

pickle_data = pickle.load(open("pickle_dump/training_data.pickle", "rb"))
vocabulary = pickle_data['vocabulary']
bow = pickle_data['w_bow']
classes = bow.keys()

ERROR_THRESHOLD = 0.2

########################################
# Function Defintions
########################################


def predictAllIntents(query, filtered_intents, debug_level):

    # Catch empty strings (Dead code, but should catch new implementations)
    if not query:
        return [('noanswer', 1)]

    # init
    sim_data = dict.fromkeys(filtered_intents)
    vector_query = np.zeros(len(vocabulary))

    # Clean query
    cleaned_query = kiwibot_mu.clean_general_query(query)

    if debug_level >= 3:
        print("Cleaned query:", cleaned_query)

    # Handle stopwords
    if not cleaned_query:
        return [('stopwords', 1)]

    # Vectorize query according to our bag of words
    for word in cleaned_query:
        try:
            index = vocabulary.index(word)
            vector_query[index] += 1
        except ValueError:
            continue

    # Catch zero-vectors, otherwise scipy.spatial.distance.cosine throws an error
    if not np.any(vector_query):
        return [('undefined', 1)]

    # Apply term weighting to the vectorized query
    vector_query = kiwibot_mu.logfreq_weighting(vector_query)

    # Calculate similarity measure against each class
    for intent in filtered_intents:
        sim_data[intent] = kiwibot_mu.sim_cosine(bow[intent], vector_query)

    # Sort the predicted classes by similarity
    sorted_sim_data = sorted(
        sim_data.items(), key=lambda item: item[1], reverse=True)

    # Debug
    if debug_level >= 4:
        for prediction in sorted_sim_data:
            print(f'Sim w/ {prediction[0]}: {prediction[1]}')

    # Catch if highest prediction below error threshold
    if list(sorted_sim_data)[0][1] < ERROR_THRESHOLD:
        return [('uncertain', 1)]

    # Catch close predictions [Not very important to catch]
    # closest_pred_d = abs(sorted_sim_data[0][1] - sorted_sim_data[1][1])
    # if closest_pred_d < ERROR_THRESHOLD:
    #     print(closest_pred_d)
    #     return [('close_predictions', 1)]

    # print(sorted_sim_data)
    return sorted_sim_data


def predictLikeliestIntent(query, filtered_intents, debug_level):
    allIntents = predictAllIntents(query, filtered_intents, debug_level)
    return list(allIntents)[0][0]
