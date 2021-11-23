from nltk.stem import WordNetLemmatizer
from docbot import interface as docbot_ui
from docbot import response as docbot_resp

# Desc: Main entry point executable for docbot

# Run lemmatizer once at init; if not, then there is noticeable delay only on Docbot's first response. Weird.
# Run a print statement before and after this code block, you can see the time delay.
# print("before instantiation")
lemmatizer = WordNetLemmatizer()
# print("after instantiation")
lemmatizer.lemmatize("")
# print("after lemma")

# Header
print(docbot_ui.green(
    "\n###################################################################################"))
print(docbot_ui.green(
    "################################### D O C B O T ###################################"))
print(docbot_ui.green(
    "###################################################################################"))

# Greet user
DOC_GREETING = [
    "Hello, my name is DocBot! I am a chatbot assistant for computer programmers.",
    "I know a lot about your favorite programming languages!",
    # "For example, ask me about the 'random' module in Python..."
    "What's your name? (Case-sensitive; I take usernames!)"
]
docbot_ui.docbot_says(DOC_GREETING)

# Initialize
terminate = False
my_docbot = docbot_resp.DocBot()

# Main while loop
while not terminate:
    query = docbot_ui.user_says()
    terminate = my_docbot.gen_response(query)

# Footer
print(docbot_ui.green(
    "\n###################################################################################"))
print(docbot_ui.green(
    "############################################################################ docbot\n"))
