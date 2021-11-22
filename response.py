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

# Load context filters
filter_list = {}
for intent in intents_file['intents']:
    if ('context' in intent):
        filter_list[intent['tag']] = intent.get('context').get('filter')


########################################
# Response Management
########################################


def genResponse(query):

    # Predict classes with the query
    predictedClass = docbot_pred.predictAllIntents(query)

    filtered_intents = []
    for intent in filter_list:

        if context == filter_list[intent]:
            filtered_intents.append(intent)

    #! CONTEXT SWITCHING HERE

    responses = []
    # Obtain the corresponding data from the json data
    for intent in intents_file['intents']:
        if intent['tag'] == predictedClass:
            responses.append(random.choice(intent['responses_1']))
            if 'responses_2' in intent:
                responses.append(random.choice(intent['responses_2']))
            if 'responses_3' in intent:
                responses.append(random.choice(intent['responses_3']))
            if 'context' in intent:
                intent_context = intent['context']
            # if 'responses_4' in intent:
            #     responses.append(random.choice(intent['responses_2']))

    # Return response to user
    docbot_ui.docbot_says(responses)

    # function application

    return (predictedClass == 'goodbye')


genResponse("hello")

# print(next(key for key, value in intent.iteritems() if value == "prompt_name"))
