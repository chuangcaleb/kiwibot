import re
from nltk.tokenize import sent_tokenize
import wikipedia
import requests.exceptions

# So in the wikipedia package, wikipedia.py prints a GuessedAtParserWarning in prompt
# when wikpedia.summary returns a disambiguation. There is no way on my side to
# fix the problem, and since the warning uglily prints in console/terminal where
# the chatbot is, I have no choice but to ignore the warning
import warnings
warnings.filterwarnings("ignore")


def wikipedia_search(bot, search_query, is_random=False):

    try:
        raw_summary = wikipedia.summary(
            search_query, sentences=3, auto_suggest=is_random)
        cleaned_summary = re.sub(r"([\n])+", "", raw_summary)
        responses = sent_tokenize(cleaned_summary)

        # Always return three responses, no matter how many sentences.
        # If not, this breaks $DISAMB in regex
        responses = responses[:3]

        bot.context = 'active_topic'

        # TODO: ask for what next
        # responses.append("")
    except wikipedia.exceptions.DisambiguationError as e:
        bot.DISAMB = e.options[:3]
        responses = bot.pull_responses('search_disamb')
    except wikipedia.exceptions.PageError:
        responses = bot.pull_responses('search_result_empty')
    except (wikipedia.exceptions.HTTPTimeoutError, requests.exceptions.ConnectionError):
        responses = bot.pull_responses('search_timeout_error')

    return responses


def wikipedia_random_search(bot):

    try:
        page = wikipedia.random()
        responses = wikipedia_search(bot, page, is_random=True)
    # If random page gets disambiguated (so weird), try random search again
    except (wikipedia.exceptions.PageError, AttributeError):
        # print("Hold on...")
        return wikipedia_random_search(bot)

    return responses
