import os, csv, pickle
from utils import preprocessing_nltk
from utils import compute_tfidf

class CSV2Dict:
	def __init__(self, dataset, delimiter=' ', quotechar='\'', splittsv=None, topickle=None):
		assert os.path.isfile(dataset)

		self.dataset = dataset
		self.store_pickle = 'store.pkl'
		self.delimiter = delimiter
		self.quotechar = quotechar
		self.splittsv = splittsv
		self.topickle = topickle

		# tsv/ folder has to be created if it doesn't exist
		if self.splittsv is not None:
			if not os.path.isdir(self.splittsv):
				os.mkdir(self.splittsv)

	def __save_as_pickle(self, save_location, data):
		print('Saving as pickle: ' + save_location + self.store_pickle)

		# create folder if does not exist
		if not os.path.isdir(save_location):
			os.mkdir(save_location)

		with open(save_location + self.store_pickle, 'wb') as handle:
			pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

	def __load_from_pickle(self, load_location):
		print('Loading from pickle: ' + load_location + self.store_pickle)

		with open(load_location + self.store_pickle, 'rb') as handle:
			return pickle.load(handle)

	# processing the main .csv and creating a no. of .tsv (if needed)
	def __get_data(self):

		# it simply is the document content
		docid2words = {}

		# vocabulary
		word2id = {}

		# documents that contain a precise word
		word2docid = {}

		# a collection of city, coords and document id
		geo2coords = {}

		# document id related to the city name
		docid2geo = {}

		with open(self.dataset, 'r', encoding='utf8') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=self.delimiter, quotechar=self.quotechar)
			
			# extracting data from each line
			for i, elems in enumerate(csvreader): # line
			
				# skip header
				if i == 0: continue
				
				# file index
				index = elems[0]
				
				# geo (coords and city)
				coords = (elems[6], elems[7])
				city = elems[3]
				
				# preprocessing content (words)
				descr = preprocessing_nltk(elems[5])
				title = preprocessing_nltk(elems[8])
				
				# discarding docs with no words...
				if len(descr) == 0 and len(title) == 0: continue
				
				# we don't want to deal with no location (needed in step 4)
				if all(isinstance(c, float) for c in coords): continue  
				
				# add city and its coords (no duplicates)
				if not city in geo2coords.keys():
					geo2coords[city] = coords       

				# docid2geo
				docid2geo[index] = city
				
				# docid2words
				docid2words[index] = []
				docid2words[index].extend(descr)
				docid2words[index].extend(title)
				
				# working with words to fill dictionaries
				for word in docid2words[index]:
					
					# word2id
					if not word in word2id.keys(): 
						word2id[word] = len(word2id.keys())
					
					# word2docid
					if not word in word2docid.keys():
						word2docid[word] = set([index])
					else:
						word2docid[word].add(index)
				
				# produce tsv if True
				if self.splittsv is not None:

					# put .tsv files into 'tsv' folder (that already has to exist)
					with open(self.splittsv + 'doc_' + index + '.tsv', 'w', encoding='utf8') as doc_out:
						doc_out.write('\t'.join(elems[1:]))

			# pack and return data
			return {
				'docid2words': docid2words,
				'word2id': word2id,
				'word2docid': word2docid,
				'geo2coords': geo2coords,
				'docid2geo': docid2geo
			}

	# todo: load/save features
	def tfidf_inverse_index(self, word2docid, docid2words):

		# inverse index
		word2docid_tfidf = {}

		# docid2words_tfidf
		docid2words_tfidf = {}

		# create inverse index with tfidf
		for w, docs in word2docid.items():
			
			# skip in case we already have a word in the vocabulary
			if w in word2docid_tfidf.keys(): continue
			
			# empty list (of future tuples)
			word2docid_tfidf[w] = []
			
			# for each document that contains w
			for d in docs:
				
				# create an empty structure if it's the first match
				if not d in docid2words_tfidf.keys():
					docid2words_tfidf[d] = {}
				
				# get document words (all its words)
				content = docid2words[d]
				
				# compute tfidf
				tfidf = compute_tfidf(content.count(w), len(content), len(docid2words.keys()), len(docs))
				
				# fill the vector
				word2docid_tfidf[w].append((d, tfidf))
				docid2words_tfidf[d][w] = tfidf

		return {
			'word2docid_tfidf': word2docid_tfidf,
			'docid2words_tfidf': docid2words_tfidf
		}

	def init(self):

		# load if pickle location has been provided
		if self.topickle is not None:
			if self.topickle[0] == 'load':
				if os.path.isfile(self.topickle[1] + self.store_pickle):
					return self.__load_from_pickle(self.topickle[1])

		# process file and get data
		data = self.__get_data()

		# store as pickle(s) file
		if self.topickle is not None:
			if self.topickle[0] == 'save':
				self.__save_as_pickle(self.topickle[1], data)

		return data
					   