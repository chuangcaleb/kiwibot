from nltk.stem import WordNetLemmatizer
from docbot import interface as docbot_ui
from docbot import response as docbot_resp

# Desc: Main entry point executable for docbot

#! Run lemmatizer once at init; if not, then there is noticeable delay only on Docbot's first response. Weird.
# Run a print statement before and after this code block, you can see the time delay.
# print("before instantiation")
lemmatizer = WordNetLemmatizer()
# print("after instantiation")
lemmatizer.lemmatize("")
# print("after lemma")

#!
#!
#! REMEMBER TO UNCOMMENT sleep() on interface.py
#! and update intents>undefined>responses_1
#!
#!

# Print Header
print(docbot_ui.green(
    "\n###################################################################################"))
print(docbot_ui.green(
    "################################### D O C B O T ###################################"))
print(docbot_ui.green(
    "###################################################################################"))

# Initialize
terminate = False
my_docbot = docbot_resp.DocBot()


# Main while loop
while not terminate:
    query = docbot_ui.user_says()
    terminate = my_docbot.gen_response(query)

# Print Footer
print(docbot_ui.green(
    "\n###################################################################################"))
print(docbot_ui.green(
    "############################################################################ docbot\n"))
