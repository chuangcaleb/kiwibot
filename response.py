# Mangages the response of the chatbot according to the predicted class

import prediction as docbot_pred
import interface as docbot_ui
import json
import random


########################################
# Response Management
########################################


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
    # Context switching
    ########################################
    def contextSwitch(self, context):
        switch = {
            'prompt_name': self.prompt_name(),
        }
        return switch.get(context, 'Not a valid context')

    def prompt_name(message):
        return print(message)

    ########################################
    # Main Method
    ########################################
    def genResponse(self, query):
        print("Current context: ", self.context)

        # Get intents with matching context
        filtered_intents = []
        for intent in self.filter_list:
            if self.context == self.filter_list[intent]:
                filtered_intents.append(intent)
        print("Current intents: ", filtered_intents)

        # If only one matching intent/context, then force it
        if len(filtered_intents) == 1:
            predictedClass = [x for x in self.intents_file.get(
                'tag').get('filter') if x == filtered_intents.item()]
        # Else, predict classes with the query, but only the subset filtered intent classes
        else:
            predictedClass = docbot_pred.predictLikeliestIntent(
                query, filtered_intents)
        # print("Predicted class: ", predictedClass)

        # Obtain the corresponding data from the json data
        responses = []
        for intent in self.intents_file['intents']:
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

        #! CONTEXT SWITCHING HERE

        # Return response to user
        docbot_ui.docbot_says(responses)

        # function application

        return (predictedClass == 'goodbye')
