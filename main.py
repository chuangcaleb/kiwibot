from nltk.stem import WordNetLemmatizer
import interface as docbot_ui
import response as docbot_resp

# Desc: Main entry point executable for docbot

# Run lemmatizer once at init; if not, then there is noticeable delay on the first response only. Weird.
lemmatizer = WordNetLemmatizer()
lemmatizer.lemmatize("hi")

print(docbot_ui.green(
    "\n###################################################################################"))

DOC_GREETING = [
    "Hello, my name is DocBot! I am a chatbot assistant for computer programmers.",
    "I know a lot about your favourite programming languages!",
    "For example, ask me about the 'random' module in Python..."
    # "What's your name?"
]

docbot_ui.docbot_says(DOC_GREETING)

terminate = False

while not terminate:

    query = docbot_ui.user_says()
    docbot_resp.genResponse(query)
