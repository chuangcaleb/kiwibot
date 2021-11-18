# Mangages the response of the chatbot according to the predicted class

import prediction as docbot_pred
import interface as docbot_ui
import json
import random

########################################
# Load variables
########################################

data_file = open('intents.json').read()
intents_file = json.loads(data_file)


########################################
# Response Management
########################################

def genResponse(query):

    # Predict the class with the query
    predictedClass = docbot_pred.predictLikeliestIntent(query)

    # Obtain the possible responses from the json data
    for intent in intents_file['intents']:
        if intent['tag'] == predictedClass:
            all_responses = intent['responses']

    # Pick a random response from the list
    response = [random.choice(all_responses)]

    # Return response to user
    docbot_ui.docbot_says(response)
