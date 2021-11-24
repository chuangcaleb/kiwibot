# Mangages the response of the chatbot according to the predicted class

from docbot import prediction as docbot_pred
from docbot import interface as docbot_ui
import json
import random
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle
from nltk.stem.snowball import SnowballStemmer

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
                       ["tell", "what", "about", "is", "in", "does", "python", "java", "mean"])
# english_stopwords.extend(['docbot', 'doc'])

# Load glossaries
python_glossary = pickle.load(
    open("pickle_dump/python_glossary.pickle", "rb"))
java_glossary = pickle.load(
    open("pickle_dump/java_glossary.pickle", "rb"))


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
        self.QUERY = ''
        self.LANG = ''

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

    def gen_response(self, raw_query):

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
                raw_query, filtered_intents, self.debug_level)

        # Debug
        if self.debug_level >= 1:
            print("Predicted intent: ", predicted_intent)

        # >> Apply current context's function on the response
        responses = self.context_switch(predicted_intent, raw_query)

        # Debug
        if self.debug_level >= 4:
            print("Responses before regex sub: ", responses)

        # >> Apply regex on responses
        responses = self.apply_regex(responses)

        # >> Return response to user
        docbot_ui.docbot_says(responses)

        return (predicted_intent == 'goodbye')

    ########################################
    # Context switching helper functions
    ########################################

    # Switch function to apply based on query
    def context_switch(self, predicted_intent, raw_query):

        # if query is empty, force 'noanswer'
        if not raw_query:
            return self.pull_responses('noanswer')

        # Switch dictionary of all possible context functions
        context_switcher = {
            'prompt_name': lambda: self.process_name(predicted_intent, raw_query),
            'query_py': lambda: self.process_search(raw_query, "Python"),
            'query_jv': lambda: self.process_search(raw_query, "Java"),
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

        return responses

    def apply_regex(self, responses):
        # >> Apply regex on response
        formatted_responses = []
        for response in responses:
            # $NAME
            formatted_response = re.sub(r'\$NAME', self.NAME, response)
            # $QUERY
            formatted_response = re.sub(
                r'\$QUERY', self.QUERY, formatted_response)
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

    def clean_search_query(self, query):

        # tokenize query
        tok_query = word_tokenize(query)

        # lowercase and stopwords
        filtered_query = [word.lower() for word in tok_query
                          if word.lower() not in english_stopwords]

        # Stemming
        cleaned_query = [snowball_stemmer.stem(
            word) for word in filtered_query]

        return cleaned_query

    def process_search(self, raw_query, language):

        # filter english_stopwords out of query
        search_words = self.clean_search_query(raw_query.strip(".,!?"))
        search_query = " ".join(search_words)

        # If search query is made up of only stopwords
        if len(search_words) == 0:
            responses = self.pull_responses('stopwords')
            return responses

        # If user enters "nevermind"
        if "".join(search_words) == 'nevermind':
            return self.pull_responses('pop_to_general')

        # Set memory variables
        self.QUERY = " ".join(
            [word for word in word_tokenize(raw_query) if word not in search_stopwords])
        self.LANG = language

        responses = []

        # TODO: Switch according to language (to refactor)
        if language == 'Python':
            for term in python_glossary:
                if search_query == term.lower():
                    responses = python_glossary[term]
                    first_response = f"This is what I know about a '{term}' in {self.LANG}!"
                    responses = [first_response] + responses
        elif language == 'Java':
            for term in java_glossary:
                if search_query == term.lower():
                    responses = java_glossary[term]
                    first_response = f"This is what I know about '{term}' in {self.LANG}!"
                    responses = [first_response] + responses
        else:
            # User should never get here, only a dev error
            print("ERROR: Unrecognized language!")

        if not responses:  # If responses is still empty, say "I don't know"
            self.QUERY = raw_query
            responses = self.pull_responses('search_result_empty')

        return responses
