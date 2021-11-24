from bs4 import BeautifulSoup
from urllib import request
from nltk.tokenize import sent_tokenize
import pickle

url = "https://docs.python.org/3/glossary.html"
html_doc = request.urlopen(url).read().decode('utf8', errors='ignore')


soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup.body.prettify())

keywords = [keyword.get_text()
            for keyword in soup.find_all('dt')]
definitions = [sent_tokenize(description.get_text().replace("\n", " "))
               for description in soup.find_all('dd')]


python_glossary = dict(zip(keywords, definitions))

for item in python_glossary:
    print(item)
    print(python_glossary[item])
    print("\n----\n")


pickle.dump(python_glossary, open("pickle_dump/python_glossary.pickle", "wb"))
