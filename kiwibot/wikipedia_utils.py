from nltk.tokenize import sent_tokenize
import wikipedia
import requests.exceptions
import random


def wikipedia_search(bot, search_query, is_random=False):

    try:
        responses = sent_tokenize(
            wikipedia.summary(search_query, sentences=3, auto_suggest=is_random))[:3]  # Limit to first three results, pages like "Jerry H. Bilik" pulls more sentences
        # TODO: ask for what next
        # responses.append("")
    except wikipedia.exceptions.DisambiguationError as e:
        bot.DISAMB = e.options[:3]
        responses = bot.pull_responses('search_disamb')
    except wikipedia.exceptions.PageError:
        responses = bot.pull_responses('search_result_empty')
    except (wikipedia.exceptions.HTTPTimeoutError, requests.exceptions.ConnectionError):
        responses = bot.pull_responses('search_timeout_error')

    print(responses)
    return responses


def wikipedia_random_search(bot):

    try:
        responses = wikipedia_search(bot, wikipedia.random(), is_random=True)
    # If random page gets disambiguated (so weird), try random search again
    except (wikipedia.exceptions.PageError, AttributeError):
        print("Hold on...")
        return wikipedia_random_search(bot)

    return responses
