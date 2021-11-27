from nltk.stem import WordNetLemmatizer
import nltk.downloader

from kiwibot import interface as kiwibot_ui
from kiwibot import response as kiwibot_resp

# Desc: Main entry point executable for kiwibot

# Download NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

#! Run lemmatizer once at init; if not, then there is noticeable delay only on kiwibot's first response. Weird.
# Run a print statement before and after this code block, you can see the time delay.
# print("before instantiation")
lemmatizer = WordNetLemmatizer()
# print("after instantiation")
lemmatizer.lemmatize("")
# print("after lemma")

# Print Header
print(kiwibot_ui.green(
    "\n###################################################################################"))
print(kiwibot_ui.green(
    "################################# K I W I B O T ###################################"))
print(kiwibot_ui.green(
    "###################################################################################"))

# Initialize
terminate = False
my_kiwibot = kiwibot_resp.KiwiBot(debug_level=0)


# Main while loop
while not terminate:
    query = kiwibot_ui.user_says()
    terminate = my_kiwibot.gen_response(query)

# Print Footer
print(kiwibot_ui.green(
    "\n###################################################################################"))
print(kiwibot_ui.green(
    "########################################################################### kiwibot\n"))
