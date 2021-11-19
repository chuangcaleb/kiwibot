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

# On startup, set context to prompt name
context = 'prompt_name'


########################################
# Response Management
########################################

def genResponse(query):

    # Predict the class with the query
    predictedClass = docbot_pred.predictLikeliestIntent(query)

    responses = []
    # Obtain the possible responses from the json data
    for intent in intents_file['intents']:
        if intent['tag'] == predictedClass:
            responses.append(random.choice(intent['responses_1']))
            if 'responses_2' in intent:
                responses.append(random.choice(intent['responses_2']))
            if 'responses_3' in intent:
                responses.append(random.choice(intent['responses_3']))
            # if 'responses_4' in intent:
            #     responses.append(random.choice(intent['responses_2']))

    # Return response to user
    docbot_ui.docbot_says(responses)
    return (predictedClass == 'goodbye')
