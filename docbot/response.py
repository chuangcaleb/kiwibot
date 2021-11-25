# Mangages the response of the chatbot according to the predicted class

from docbot import prediction as docbot_pred
from docbot import interface as docbot_ui
import json
import random
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.snowball import SnowballStemmer
import wikipedia
import string

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
english_stopwords = stopwords.words('english')
search_stopwords = set(english_stopwords +
                       ["tell", "who", "what", "about", "is", "in", "does", "mean"])


class DocBot(object):

    ########################################
    # Init variables
    ########################################

    def __init__(self, debug_level=0):

        # Debug level
        self.debug_level = debug_level
        # On startup, set context to prompt name
        self.context = 'prompt_name'
        # self.context = 'prompt_name'
        self.NAME = ''
        self.RAW_QUERY = ''
        self.LANG = ''

        if self.debug_level >= 1:
            print(docbot_ui.red(
                f"\nDEBUGGING ENABLED: DocBot at debug level {self.debug_level}"))

        # Greet user
        DOC_GREETING = [
            "Hello, my name is Kiwi! I am a knowledge-base information-retrieval chatbot.",
            "I know a lot about a lot of things! But first!",
            "What's your name? (Case-sensitive!)"
        ]
        docbot_ui.docbot_says(DOC_GREETING)

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

            predicted_intent = docbot_pred.predictLikeliestIntent(
                raw_query, possible_intents, self.debug_level)

        # Debug
        if self.debug_level >= 1:
            print("Predicted intent: ", predicted_intent)

        # >> Apply current context's function on the response
        responses = self.function_switch(predicted_intent, raw_query)

        # >> Apply regex on responses
        responses = self.apply_regex(responses)

        # >> Return response to user
        docbot_ui.docbot_says(responses)

        return (predicted_intent == 'goodbye')

    ########################################
    # Context switching helper functions
    ########################################

    # Switch function to apply based on intent
    def function_switch(self, predicted_intent, raw_query):

        # if query is empty, force 'noanswer'
        if not raw_query:
            return self.pull_responses('noanswer')

        """ Old code
        # Switch dictionary of all possible context functions
        context_switcher = {
            'prompt_name': lambda: self.process_name(predicted_intent, raw_query),
            'general': lambda: self.process_search(raw_query),
        }

        # Run the appropriate function
        # -> if context function doesn't exist, then just pull appropriate responses
        return context_switcher.get(self.context, lambda: self.pull_responses(predicted_intent))()
        #  """
        # Debug
        if self.debug_level >= 3:
            print("Predicted intent, context: ",
                  predicted_intent, self.context)

        if self.context == 'prompt_name':
            return self.process_name(predicted_intent, raw_query)
        elif predicted_intent == 'search':
            return self.process_search(raw_query)
        else:
            return self.pull_responses(predicted_intent)

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
        return responses

    def apply_regex(self, responses):

        # Debug
        if self.debug_level >= 4:
            print("Responses before regex sub: ", responses)

        # >> Apply regex on response
        formatted_responses = []
        for response in responses:
            # $NAME
            formatted_response = re.sub(r'\$NAME', self.NAME, response)
            # $QUERY
            formatted_response = re.sub(
                r'\$QUERY', self.RAW_QUERY, formatted_response)
            # $LANG
            formatted_response = re.sub(
                r'\$LANG', self.LANG, formatted_response)
            # Append
            formatted_responses.append(formatted_response)

        return formatted_responses

    ########################################
    # Context-specific functions
    ########################################

    def process_name(self, predicted_intent, raw_query):

        name_stopwords = ["my", "name", "is",
                          "the", " ", "i'm", "i", "am", "me", "name's", "they", "call"]
        name_stopwords.extend(english_stopwords)
        # filter name out of query
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

    # Clean search query:
    #   - tokenize
    #   - lowercase
    #   - english_stopwords
    #   - stem

    def process_search(self, raw_query):

        # filter english_stopwords out of query
        search_words = [word.lower() for word in word_tokenize(
            raw_query) if word.lower() not in search_stopwords]
        search_query = " ".join(search_words)

        # Debug
        if self.debug_level >= 3:
            print("Cleaned search query: ", search_query)

        # If search query is made up of only stopwords
        if len(search_words) == 0:
            responses = self.pull_responses('stopwords')
            return responses

        # If user enters "nevermind"
        if "".join(search_words) == 'nevermind':
            return self.pull_responses('pop_to_general')

        # Set memory variables
        # Include english_stopwords and
        self.RAW_QUERY = " ".join(
            [word for word in word_tokenize(raw_query) if word not in search_stopwords])

        responses = []
        responses = sent_tokenize(wikipedia.summary(search_query, sentences=3))

        if not responses:  # If responses is still empty, say "I don't know"
            self.RAW_QUERY = raw_query
            responses = self.pull_responses('search_result_empty')

        return responses
