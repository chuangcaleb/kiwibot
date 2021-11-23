# Mangages the response of the chatbot according to the predicted class

from docbot import prediction as docbot_pred
from docbot import interface as docbot_ui
import json
import random
import re
import string


data_file = open('intents.json').read()
intents_file = json.loads(data_file)

# Load context filters and all filters
filter_list = {}
for intent in intents_file['intents']:
    # self.all_intents.append(intent.get('context').get('filter'))
    if ('context' in intent):
        filter_list[intent['tag']] = intent.get(
            'context').get('filter')


class DocBot():

    ########################################
    # Init variables
    ########################################

    def __init__(self):

        # On startup, set context to prompt name
        self.context = 'prompt_name'

    ########################################
    # Main Method
    ########################################

    def gen_response(self, query):

        print("Current context: ", self.context)

        # Get intents with matching context
        filtered_intents = []
        for intent in filter_list:
            if self.context == filter_list[intent]:
                filtered_intents.append(intent)
        print("Possible intents: ", filtered_intents)

        # >> Retrieving appropriate intents
        # If only one matching intent/context, then force it
        if len(filtered_intents) == 1:
            predicted_intent = filtered_intents[0]
        # Else, predict intent with the query, but only the subset filtered intent classes
        else:
            predicted_intent = docbot_pred.predictLikeliestIntent(
                query, filtered_intents)
        print("Predicted intent: ", predicted_intent)

        # Apply current context's function on the response
        responses = self.context_switch(predicted_intent, query)

        # Return response to user
        docbot_ui.docbot_says(responses)

        return (predicted_intent == 'goodbye')

    ########################################
    # Context switching helper functions
    ########################################

    def pull_responses(self, predicted_intent):
        # Obtain the corresponding data from the json data
        responses = []
        for intent in intents_file['intents']:
            if intent['tag'] == predicted_intent:
                responses.append(random.choice(intent['responses_1']))
                if 'responses_2' in intent:
                    responses.append(random.choice(intent['responses_2']))
                if 'responses_3' in intent:
                    responses.append(random.choice(intent['responses_3']))
                if 'context' in intent:
                    intent_context = intent['context']
                # if 'responses_4' in intent:
                #     responses.append(random.choice(intent['responses_2']))
        return responses

    # Switch function to apply based on query
    def context_switch(self, predicted_intent, query):

        # if query is empty, force 'noanswer'
        if not query:
            return self.pull_responses('noanswer')

        switch = {
            'prompt_name': self.prompt_name(predicted_intent, query),
        }

        return switch.get(self.context)

    ########################################
    # Context functions
    ########################################

    def prompt_name(self, predicted_intent, query):

        name_stopwords = ["my", "name", "is",
                          "the", " ", "i'm", "i", "am", "me", "name's", "they", "call"]
        # filter name out of query
        names = [word.strip(".,!") for word in query.split(
            " ") if word.lower() not in name_stopwords]
        filtered_query = " ".join(names)

        if not re.match(r"^[a-zA-Z\ ]+$", filtered_query):  # If invalid symbols
            responses = self.pull_responses('invalid_name')
        else:  # Else, a legit name input
            # pull old responses
            responses = self.pull_responses(predicted_intent)

        # Apply regex on response
        formatted_responses = []
        for response in responses:
            formatted_responses.append(
                re.sub(r'\$NAME', filtered_query, response))

        return formatted_responses

# my_docbot = DocBot()
# # my_docbot.gen_response("Caleb")
# filtered_intents = ['greet_name']
# thing = my_docbot.filter_list.get(filtered_intents[0])
# print(thing)
