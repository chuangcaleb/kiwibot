# Utils file for calculation function definitions that are shared by many files

from math import log10

from nltk.tokenize import word_tokenize
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from scipy import spatial


lemmatizer = WordNetLemmatizer()
# Remove stopwords, lowercase
ignore_words = [',', "!"]

english_stopwords = stopwords.words('english')
meaningful_stopwords = ["my", "your", "i",
                        "you", "how", "are", "who", "what", "is", "me", "about"]
for word in meaningful_stopwords:
    english_stopwords.remove(word)

ignore_words.extend(english_stopwords)


# Term weighing function
def logfreq_weighting(vector):
    lf_vector = []
    for frequency in vector:
        lf_vector.append(log10(1+frequency))
    return np.array(lf_vector)


# Cosine similarity function
def sim_cosine(vector_1, vector_2):
    similarity = 1 - spatial.distance.cosine(vector_1, vector_2)
    return similarity


# Clean query:
#   - tokenize
#   - lowercase
#   - ignore_stopwords
#   - lemmatize
def clean_general_query(query):

    # tokenize query
    tok_query = word_tokenize(query)

    # lowercase and stopwords
    filtered_query = [word.lower() for word in tok_query
                      if word.lower() not in ignore_words]

    # Lemmatising
    cleaned_query = [lemmatizer.lemmatize(word) for word in filtered_query]

    return cleaned_query
