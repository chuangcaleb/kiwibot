# %% [markdown]
# # **HAI Coursework 1: AN INTERACTIVE NLP-BASED AI SYSTEM**
#
# ## Project Title: Chatbot Assistant for Computer Programmers
#
# 20204134 Chuang Caleb hcycc2
#
# BSc Hons Computer Science with Artificial Intelligence
#
# ---
#

# %% [markdown]
# ## **INITIALIZATION**
#
# ### Imports

# %%
# External python modules/packages
import nltk

# My own python modules
# from utils.my_global import *


# %% [markdown]
# ### Global declarations!
#

# %%
# Global Chat
colors = {
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'grey': '\033[90m',
    'white': '\033[97m',
    'end': '\033[0m',
}


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


def docbot_says(message):
    return print(green(f"{message}"))


def user_says():
    print()
    return input()


# %% [markdown]
# ---
#
# ## Greeting

# %%
docbot_says(
    f"Hello, my name is DocBot! I am a chatbot assistant for computer programmers!")
docbot_says("What's your name?")
q = user_says()
print(f"My name is: {q}")
