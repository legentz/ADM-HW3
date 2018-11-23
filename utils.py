import numpy as np
import math
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from scipy import spatial
import geopy.distance

# stopwords
stopwords = set(stopwords.words('english'))

# from https://stackoverflow.com/questions/21030391/how-to-normalize-array-numpy
def normalized(a, axis=-1, order=2):
	l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
	l2[l2==0] = 1
	return a / np.expand_dims(l2, axis)

# cleaning stuff
def preprocessing_nltk(e):
	ps = PorterStemmer()
	
	e = e.lower().replace('\n', '')
	e = word_tokenize(e)
	e = [w for w in e if w.isalpha()]
	e = [w for w in e if not w in stopwords]
	e = [ps.stem(w) for w in e]
	return e

def compute_tfidf(word_freq, n_words_doc, n_docs, n_docs_with_word):
	tf = word_freq / n_words_doc
	idf = math.log10(n_docs / n_docs_with_word)
	return tf * idf

def cosine_similarity(vec_src, vec_tgt):
    return 1 - spatial.distance.cosine(vec_src, vec_tgt)

# the variables of the function takes 2 values for each location
def distance_function(first_location, second_location):
    return (geopy.distance.geodesic(first_location, second_location).km) # this is better because considers the Earth as an ellipse