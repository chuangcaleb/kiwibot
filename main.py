from interface import *
from prediction import *

# Desc: Main entry point executable for docbot

global NAME
NAME = "Caleb"

print(green("\n###################################################################################"))

DOC_GREETING = [
    "Hello, my name is DocBot! I am a chatbot assistant for computer programmers.",
    "I know a lot about your favourite programming languages!",
    "For example, ask me about the 'random' module in Python..."
    # "What's your name?"
]

docbot_says(DOC_GREETING)

# NAME = user_says()

# NAME_RESPONSE = [f"Your name is: {NAME}"]

# docbot_says(NAME_RESPONSE)

terminate = False

while not terminate:

    query = user_says()
    predictLikeliestIntent(query)
