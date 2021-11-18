# Utils file for calculation function definitions that are shared by many files

from math import log10
import numpy as np
from scipy import spatial


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
