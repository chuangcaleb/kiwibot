import json
import random
import re

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize

from kiwibot import interface as kiwibot_ui
from kiwibot import prediction as kiwibot_pred
from kiwibot import wikipedia_utils as kiwibot_wk

# Mangages the response of the chatbot according to the predicted class

# Load intents
data_file = open('intents.json').read()
intents_file = json.loads(data_file)

# Load context filters
filter_list = {}
for intent in intents_file['intents']:
    if 'context' in intent:
        filter_list[intent['tag']] = intent.get(
            'context').get('filter')

# Load text processors
snowball_stemmer = SnowballStemmer("english")

# Curating custom stopwords
english_stopwords = stopwords.words('english')
search_stopwords = set(english_stopwords +
                       ["tell", "who", "me", "what", "are", "about", "is", "in", "does", "mean", "?", "know"])
name_stopwords = ["my", "name", "is",
                  "the", " ", "i'm", "i", "am", "me", "name's", "they", "call"]
name_stopwords.extend(english_stopwords)


class KiwiBot(object):

    ########################################
    # Init variables
    ########################################

    def __init__(self, debug_level=0):

        # Debug level
        self.debug_level = debug_level
        # On startup, set context to prompt name -> intent: intro takes care of it now
        self.context = ''
        self.active_page = []
        self.page_progress = 0

        self.NAME = ''
        self.RAW_QUERY = ''
        self.LANG = ''
        self.DISAMB = ['', '', '']

        if self.debug_level >= 1:
            print(kiwibot_ui.red(
                f"\nDEBUGGING ENABLED: KiwiBot at debug level {self.debug_level}"))

        # Greet user
        kiwibot_ui.kiwibot_says(self.pull_responses("intro"))

   ########################################
   # Main Method
   ########################################

    def gen_response(self, raw_query):

        # Debug
        if self.debug_level >= 2:
            print("Current context: ", self.context)

        # >> Get intents with matching context
        possible_intents = []
        for intent in filter_list:
            if self.context in filter_list[intent]:
                possible_intents.append(intent)
        # Debug
        if self.debug_level >= 3:
            print("Possible intents: ", possible_intents)
        # >> Retrieving appropriate intents
        # If only one matching intent/context, then force it
        if len(possible_intents) == 1:
            predicted_intent = possible_intents[0]

        # Else, predict intent with the query, but only the subset filtered intent classes
        else:
            predicted_intent = kiwibot_pred.predictLikeliestIntent(
                raw_query, possible_intents, self.debug_level)

        # Debug
        if self.debug_level >= 1:
            print("Predicted intent: ", predicted_intent)

        # >> Apply current context's function on the response
        responses = self.function_switch(predicted_intent, raw_query)

        # Debug
        if self.debug_level >= 2:
            print("New current context is:", self.context)

        # >> Apply regex on responses
        responses = self.apply_regex(responses)

        # >> Return response to user
        kiwibot_ui.kiwibot_says(responses)

        return (predicted_intent == 'goodbye')

    ########################################
    # Context switching helper functions
    ########################################

    # Switch function to apply based on intent
    def function_switch(self, predicted_intent, raw_query):

        # if query is empty, force 'noanswer'
        if not raw_query:
            return self.pull_responses('noanswer')

        # Switch dictionary of all possible context functions
        function_switcher = {
            'greet_name': lambda: self.process_name(predicted_intent, raw_query),
            'search': lambda: self.process_search(raw_query),
            'random': lambda: kiwibot_wk.wikipedia_random_search(self),
            'more': lambda: self.tell_more()
        }

        # Run the appropriate function
        # -> if context function doesn't exist, then just pull appropriate responses
        return function_switcher.get(predicted_intent, lambda: self.pull_responses(predicted_intent))()

    def pull_responses(self, predicted_intent):

        # >> Obtain the corresponding data from the json data
        responses = []
        for intent in intents_file['intents']:
            if intent['tag'] == predicted_intent:
                if 'responses_1' in intent:
                    responses.append(random.choice(intent['responses_1']))
                if 'responses_2' in intent:
                    responses.append(random.choice(intent['responses_2']))
                if 'responses_3' in intent:
                    responses.append(random.choice(intent['responses_3']))
                if 'responses_4' in intent:
                    responses.append(random.choice(intent['responses_4']))
                if 'responses_5' in intent:
                    responses.append(random.choice(intent['responses_5']))
                if 'context' in intent:
                    # ew such an ugly way to access
                    if 'set' in intent.get('context'):
                        self.context = intent.get('context').get('set')

        return responses

    def apply_regex(self, responses):

        # Debug
        if self.debug_level >= 4:
            print("Responses before regex sub: ", responses)

        # >> Apply regex on response
        formatted_responses = []
        for i, response in enumerate(responses):
            # $NAME
            formatted_response = re.sub(r'\$NAME', self.NAME, response)
            # $RAW_QUERY
            formatted_response = re.sub(
                r'\$RAW_QUERY', self.RAW_QUERY, formatted_response)
            # $LANG
            formatted_response = re.sub(
                r'\$LANG', self.LANG, formatted_response)
            # $DISAMB
            disamb_index = [''] + self.DISAMB + ['']
            formatted_response = re.sub(
                r'\$DISAMB', disamb_index[i], formatted_response)
            # Append
            formatted_responses.append(formatted_response)

        return formatted_responses

    ########################################
    # Context-specific functions
    ########################################

    def process_name(self, predicted_intent, raw_query):

        # extract name out of query
        names = [word.strip(".,!") for word in raw_query.split(
            " ") if word.lower() not in name_stopwords]
        full_name = " ".join(names).strip()

        # Always save user's name in instance's variable (even when reporting error)
        self.NAME = full_name

        # If invalid symbols
        if len(full_name) == 0:
            responses = self.pull_responses('stopwords')
            responses.append("Can you tell me your name?")
            return responses
        if not re.match(r"(?i)^(?:(?![×Þß÷þø])[-a-zÀ-ÿ\ \-])+$", full_name):
            return self.pull_responses('invalid_name')
        else:  # Else, a legit name input
            # pull responses as planned
            return self.pull_responses(predicted_intent)

    def process_search(self, raw_query):

        # filter english_stopwords out of query
        search_words = [word for word in word_tokenize(
            raw_query) if word.lower() not in search_stopwords]
        # If search query is made up of only stopwords
        if len(search_words) == 0:
            responses = self.pull_responses('stopwords')
            return responses

        # Join words to form search query string
        search_query = " ".join(search_words)
        # Debug
        if self.debug_level >= 3:
            print("Cleaned search query:", search_query)

        self.RAW_QUERY = " ".join(
            [word for word in word_tokenize(raw_query) if word not in search_stopwords])

        responses = kiwibot_wk.wikipedia_search(self, search_query)

        return responses

    def tell_more(self):

        # Get next index
        # Increment progress counter
        self.page_progress = self.page_progress + 3

        # Pull next three sentences
        responses = self.active_page[self.page_progress:self.page_progress+3]

        # End of extract
        if not responses:
            responses = self.pull_responses('end_of_more')

        return responses
