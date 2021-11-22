# Mangages the response of the chatbot according to the predicted class

import prediction as docbot_pred
import interface as docbot_ui
import json
import random
import re


class DocBot():

    ########################################
    # Init variables
    ########################################
    def __init__(self):
        self.data_file = open('intents.json').read()
        self.intents_file = json.loads(self.data_file)

        # On startup, set context to prompt name
        self.context = 'prompt_name'

        # Load context filters and all filters
        # self.non_filtered = []
        self.filter_list = {}
        for intent in self.intents_file['intents']:
            # self.all_intents.append(intent.get('context').get('filter'))
            if ('context' in intent):
                self.filter_list[intent['tag']] = intent.get(
                    'context').get('filter')

    ########################################
    # Main Method
    ########################################
    def gen_response(self, query):
        print("Current context: ", self.context)

        # Get intents with matching context
        filtered_intents = []
        for intent in self.filter_list:
            if self.context == self.filter_list[intent]:
                filtered_intents.append(intent)
        print("Current intents: ", filtered_intents)

        # If only one matching intent/context, then force it
        if len(filtered_intents) == 1:
            predicted_intent = filtered_intents[0]
        # Else, predict intent with the query, but only the subset filtered intent classes
        else:
            predicted_intent = docbot_pred.predictLikeliestIntent(
                query, filtered_intents)
        print("Predicted intent: ", predicted_intent)

        # Obtain the corresponding data from the json data
        responses = []
        for intent in self.intents_file['intents']:
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

        # Apply current context's function on the response
        new_responses = self.context_switch(responses, query)

        # Return response to user
        docbot_ui.docbot_says(new_responses)

        # function application

        return (predicted_intent == 'goodbye')

    def context_switch(self, responses, query):
        switch = {
            'prompt_name': prompt_name(responses, query),
        }
        return switch.get(self.context, 'Not a valid context')


########################################
# Context switching helper functions
########################################

def prompt_name(responses, query):

    new_responses = []
    for response in responses:
        new_responses.append(re.sub(r'\$NAME', query, response))
    return new_responses


# my_docbot = DocBot()
# # my_docbot.gen_response("Caleb")
# filtered_intents = ['greet_name']
# thing = my_docbot.filter_list.get(filtered_intents[0])
# print(thing)
