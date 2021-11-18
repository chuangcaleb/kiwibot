# Mangages the response of the chatbot according to the predicted class

import prediction as docbot_pred
import json

########################################
# Load variables
########################################

data_file = open('intents.json').read()
intents_file = json.loads(data_file)


########################################
# Response Management
########################################

def genResponse(query):
    predictedClass = docbot_pred.predictAllIntents(query)
    response = predictedClass
    print(response)


genResponse("hello")
