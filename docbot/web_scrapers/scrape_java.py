from bs4 import BeautifulSoup
from urllib import request
from nltk.tokenize import sent_tokenize
import pickle

url = "https://www.oracle.com/java/technologies/glossary.html"
html_doc = request.urlopen(url).read().decode('utf8', errors='ignore')

soup = BeautifulSoup(html_doc, 'html.parser')

java_glossary = {}
for strong_word in soup.find_all("strong"):
    term = strong_word.get_text().strip()
    if len(term) > 1:  # Eliminate single letter anchors
        raw_definition = strong_word.parent.next_sibling.next_sibling.get_text()
        java_glossary[term] = sent_tokenize(raw_definition)

for item in java_glossary:
    print(item)
    print(java_glossary[item])
    print("\n----\n")


pickle.dump(java_glossary, open("pickle_dump/java_glossary.pickle", "wb"))
