from interface import *
from canned_messages import *

# Desc: Main entry point executable for docbot

print(green("\n###################################################################################"))

DOC_GREETING = [
    "Hello, my name is DocBot! I am a chatbot assistant for computer programmers!",
    "What's your name?"
]

docbot_says(DOC_GREETING)

NAME = user_says()

NAME_RESPONSE = [f"Your name is: {NAME}"]

docbot_says(NAME_RESPONSE)
