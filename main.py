from nltk.stem import WordNetLemmatizer
import interface as docbot_ui
import response as docbot_resp

# Desc: Main entry point executable for docbot

# Run lemmatizer once at init; if not, then there is noticeable delay on the first response only. Weird.
# Run a print statement before and after this code block, you can see the time delay.
lemmatizer = WordNetLemmatizer()
lemmatizer.lemmatize("")

print(docbot_ui.green(
    "\n###################################################################################"))
print(docbot_ui.green(
    "################################### D O C B O T ###################################"))
print(docbot_ui.green(
    "###################################################################################"))

DOC_GREETING = [
    "Hello, my name is DocBot! I am a chatbot assistant for computer programmers.",
    "I know a lot about your favorite programming languages!",
    # "For example, ask me about the 'random' module in Python..."
    "What's your name?"
]

docbot_ui.docbot_says(DOC_GREETING)

terminate = False

docbot = docbot_resp.DocBot()

while not terminate:

    query = docbot_ui.user_says()
    terminate = docbot.gen_response(query)


print(docbot_ui.green(
    "\n###################################################################################"))
print(docbot_ui.green(
    "############################################################################ docbot\n"))
