# Mangages the response of the chatbot according to the predicted class

from docbot import prediction as docbot_pred
from docbot import interface as docbot_ui
import json
import random
import re
from nltk.corpus import stopwords
import pickle


data_file = open('intents.json').read()
intents_file = json.loads(data_file)

# Load context filters
filter_list = {}
for intent in intents_file['intents']:
    if 'context' in intent:
        filter_list[intent['tag']] = intent.get(
            'context').get('filter')

english_stopwords = stopwords.words('english')

# Load python glossary
python_glossary = pickle.load(
    open("pickle_dump/python_glossary.pickle", "rb"))


class DocBot(object):

    ########################################
    # Init variables
    ########################################

    def __init__(self, debug_level=0):

        # Debug level
        self.debug_level = debug_level
        # On startup, set context to prompt name
        self.context = 'query_py'
        # self.context = 'prompt_name'
        self.NAME = ''
        self.QUERY = ''

        if self.debug_level >= 1:
            print(docbot_ui.red(
                f"\nDEBUGGING ENABLED: DocBot at debug level {self.debug_level}"))

        # Greet user
        DOC_GREETING = [
            "Hello, my name is DocBot! I am a chatbot assistant for computer programmers.",
            "I know a lot about your favorite programming languages!",
            # "For example, ask me about the 'random' module in Python..."
            "What's your name? (Case-sensitive!)"
        ]
        docbot_ui.docbot_says(DOC_GREETING)

   ########################################
   # Main Method
   ########################################

    def gen_response(self, query):

        # Debug
        if self.debug_level >= 2:
            print("Current context: ", self.context)

        # >> Get intents with matching context
        filtered_intents = []
        for intent in filter_list:
            if self.context in filter_list[intent]:
                filtered_intents.append(intent)
        # Debug
        if self.debug_level >= 3:
            print("Possible intents: ", filtered_intents)

        # >> Retrieving appropriate intents
        # If only one matching intent/context, then force it
        if len(filtered_intents) == 1:
            predicted_intent = filtered_intents[0]
        # Else, predict intent with the query, but only the subset filtered intent classes
        else:
            predicted_intent = docbot_pred.predictLikeliestIntent(
                query, filtered_intents, self.debug_level)
        # Debug
        if self.debug_level >= 1:
            print("Predicted intent: ", predicted_intent)

        # >> Apply current context's function on the response
        responses = self.context_switch(predicted_intent, query)

        # >> Return response to user
        docbot_ui.docbot_says(responses)

        return (predicted_intent == 'goodbye')

    ########################################
    # Context switching helper functions
    ########################################

    # Switch function to apply based on query
    def context_switch(self, predicted_intent, query):

        # if query is empty, force 'noanswer'
        if not query:
            return self.pull_responses('noanswer')

        # Switch dictionary of all possible context functions
        context_switcher = {
            'prompt_name': lambda: self.process_name(predicted_intent, query),
            'query_py': lambda: self.process_search(predicted_intent, query, "python"),
        }

        # Run the appropriate function
        # -> if context function doesn't exist, then just pull appropriate responses
        return context_switcher.get(self.context, lambda: self.pull_responses(predicted_intent))()

    def pull_responses(self, predicted_intent):

        # >> Obtain the corresponding data from the json data
        responses = []
        for intent in intents_file['intents']:
            if intent['tag'] == predicted_intent:
                responses.append(random.choice(intent['responses_1']))
                if 'responses_2' in intent:
                    responses.append(random.choice(intent['responses_2']))
                if 'responses_3' in intent:
                    responses.append(random.choice(intent['responses_3']))
                if 'context' in intent:
                    # ew such an ugly way to access
                    if 'set' in intent.get('context'):
                        self.context = intent.get('context').get('set')
                        # Debug
                        if self.debug_level >= 2:
                            print("Changed context to:", self.context)

        # >> Apply regex on response
        formatted_responses = []
        for response in responses:
            # $NAME
            formatted_response = re.sub(r'\$NAME', self.NAME, response)
            # $QUERY
            formatted_response = re.sub(
                r'\$QUERY', self.QUERY, formatted_response)
            # Append
            formatted_responses.append(formatted_response)

        return formatted_responses

    ########################################
    # Context functions
    ########################################

    def process_name(self, predicted_intent, query):

        name_stopwords = ["my", "name", "is",
                          "the", " ", "i'm", "i", "am", "me", "name's", "they", "call"]
        # filter name out of query
        names = [word.strip(".,!") for word in query.split(
            " ") if word.lower() not in name_stopwords]
        full_name = " ".join(names)

        # Always save user's name in instance's variable (even when reporting error)
        self.NAME = full_name

        # If invalid symbols
        if not re.match(r"(?i)^(?:(?![×Þß÷þø])[-a-zÀ-ÿ\ \-])+$", full_name):
            responses = self.pull_responses('invalid_name')
        else:  # Else, a legit name input
            # pull responses as planned
            responses = self.pull_responses(predicted_intent)

        return responses

    def process_search(self, predicted_intent, query, language):

        # filter english_stopwords out of query
        keywords = [word.strip(".,!?") for word in query.split(
            " ") if word.lower() not in english_stopwords]
        search_query = " ".join(keywords)

        self.QUERY = search_query

        if language == 'python':
            for keyword in python_glossary:
                if search_query == keyword:
                    print(python_glossary[keyword])
            print("end")
        else:
            print("Unrecognized language!")

        # pull responses as planned
        responses = self.pull_responses(predicted_intent)

        return responses
