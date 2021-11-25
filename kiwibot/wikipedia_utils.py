from nltk.tokenize import sent_tokenize
import wikipedia
import requests.exceptions


def wikipedia_search(bot, search_query):

    # Wikipedia search
    try:
        responses = sent_tokenize(
            wikipedia.summary(search_query, sentences=3, auto_suggest=False))
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
