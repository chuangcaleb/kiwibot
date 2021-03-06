import time

from nltk.tokenize import word_tokenize

# Handles chat display appearances i.e. what the user sees

# Global Chat
colors = {
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'grey': '\033[90m',
    'white': '\033[97m',
    'end': '\033[0m',
}

TIME_MULTIPLIER = 0.1


def green(message):
    return f"{colors['green']}{message}{colors['end']}"


def yellow(message):
    return f"{colors['yellow']}{message}{colors['end']}"


def red(message):
    return f"{colors['red']}{message}{colors['end']}"


def grey(message):
    return f"{colors['grey']}{message}{colors['end']}"


def white(message):
    return f"{colors['white']}{message}{colors['end']}"


def kiwibot_says(message):

    print()

    for string in message:
        variable_sleep(string)
        print(green(f"[Kiwi] {string}"))


def variable_sleep(string):

    if TIME_MULTIPLIER:
        words = len(word_tokenize(string))
        delay = words * TIME_MULTIPLIER
        time.sleep(delay)


def user_says():
    print()
    return input(yellow("> "))
