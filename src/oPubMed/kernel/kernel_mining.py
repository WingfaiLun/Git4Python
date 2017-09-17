# Created by Tony HAO, th2510@columbia.edu

from NLP import sentence as NLP_sent
from NLP import word as NLP_word
from NLP import porter2
import utility
import string, math


#============================================================Method: N-gram - based generation

# generate ngrams from a single document
def Generate_ngrams_document (text, max_num, stop, use_pos, ptag, use_stem, split, all_pos_tags):
	
	doc_ngrams = {}
	sentences = []
	if split is None:
		sentences = NLP_sent.sentence_splitting(text, 1)
	else:
		can_sens = text.split(split)
		for can_sen in can_sens:
			sentences.extend(NLP_sent.sentence_splitting(can_sen, 1))
					
	for sentence in sentences:
		phrases = NLP_sent.phrase_splitting(sentence)		
		for phrase in phrases:
			if len(phrase) <= 2: # e.g.'ii'
				continue
			
			words = NLP_word.word_splitting(phrase.lower())
			if (use_pos):
				if phrase in all_pos_tags:
					pos_tags = all_pos_tags[phrase]
				else:
					pos_tags = NLP_word.word_pos_tagging(words)
					all_pos_tags[phrase] = pos_tags
			
			stop_pos = [] # record all positions of stop  or non-preferred (POS) words in the phrase to increase efficiency
			for i in xrange(len(words)):
				type = word_checking_stop(words[i], stop)
				stop_pos.append(type)
				if use_stem: # enable or disable stemming
					words[i] = porter2.stem(words[i])
			
#  			if  "patients who underwent" in phrase:
#  				print "aa"
			for i in xrange(len(words)):
				if 0 < stop_pos[i] < 5:
					continue
				for j in xrange(i+1, min(len(words), i+max_num)+1):
					if 0 < stop_pos[j-1] < 5:# check validity
						continue
 					meaningful_word = False
 					if (j == i +1):
 						if (stop_pos[i] == 0) and (not use_pos or (use_pos and word_checking_pos(pos_tags[i], ptag) == 0)):
 							meaningful_word = True
 					else:  
#  						if (use_pos and word_checking_pos(pos_tags[j-1], ptag) == 1):
#  							continue		
						mless_num = 0		
						for k in xrange(i,j):
							if stop_pos[k] ==0 or stop_pos[k]==5:
								meaningful_word =True
							else:
								mless_num +=1
						if mless_num>=(j-i-1):
							continue
  					if (meaningful_word):
						ngram = ' '.join(words[i:j])
						if len(ngram)>1: # at least two characters
							if (ngram in doc_ngrams):
									doc_ngrams[ngram] += 1
							else:
								doc_ngrams[ngram] = 1
		
	return doc_ngrams		
				
	
# get frequent ngrams
def Get_frequent_ngrams (ngrams, threshold):
	# retain the most frequent ngrams by comparing with threshold number
	for key in ngrams.keys():
		if ngrams[key] < threshold:
			del ngrams[key]
	return ngrams


# check if a word is in the POS list
def word_checking_pos(pos_tag, ptag):
	if pos_tag[1] in ptag: 
		return 1
	else:
		return 0
	
	
# remove ngrams with same words but in different sequence
def sequence_filtering (ngrams):
	sorted_ngrams = sorted(ngrams.keys(), key=len)
	all_keys = ngrams.keys()
	for key in all_keys:
		for can_key in sorted_ngrams:
			if len(can_key) < len(key):
				continue
			elif len(can_key) == len(key):
				if can_key != key and set(can_key.split()) == set(key.split()):
					if ngrams[key] >= ngrams[can_key]:
						ngrams[key] += ngrams[can_key]
						del ngrams[can_key]
						all_keys.remove(can_key)
						sorted_ngrams.remove(can_key)
					else:
						ngrams[can_key] += ngrams[key]
						del ngrams[key]
						all_keys.remove(key)
						sorted_ngrams.remove(key)
					break
			else:
				break
	return ngrams



#============================================================Method: syntatic tree - based generation

import nltk
# Extract all noun phrases
def Extract_phrases_document (text, stop, split, all_pos_tags):		
	doc_phrases = {}
	sentences = []
	if split is None:
		sentences = NLP_sent.sentence_splitting(text, 1)
	else:
		can_sens = text.split(split)
		for can_sen in can_sens:
			sentences.extend(NLP_sent.sentence_splitting(can_sen, 1))
			
	for sentence in sentences:
		phrases = NLP_sent.phrase_splitting(sentence)		
		for phrase in phrases:
			if len(phrase) <= 2: # e.g.'ii'
				continue
			
			if phrase in all_pos_tags:
				pos_tags = all_pos_tags[phrase]
			else:
				#-------------------POS tagging output
				words = NLP_word.word_splitting(phrase.lower())
				pos_tags = NLP_word.word_pos_tagging(words)
				all_pos_tags[phrase] = pos_tags

	
			#-------------------parsed tree
			grammar = r"""
				NBAR:
					# Nouns and Adjectives, terminated with Nouns
					{<NN.*|JJ>*<NN.*>}
			
				NP:
					{<NBAR>}
					# Above, connected with in/of/etc...
					{<NBAR><IN><NBAR>}
			"""
	
			cp = nltk.RegexpParser(grammar, loop=2)
			cp_tree = cp.parse(pos_tags)
			terms = get_terms(cp_tree)
			for term in terms:
				phrase = ' '.join(term)
				if word_checking_stop(phrase, stop) ==0: # filter stop words
					if len(phrase)>1: # at least two characters
						doc_phrases[phrase] = 1
			
	return doc_phrases


# Ref to https://gist.github.com/879414
#from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = nltk.WordNetLemmatizer()
#stemmer = nltk.stem.porter.PorterStemmer()
from nltk.corpus import stopwords
stopwords = stopwords.words('english')

def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
#    word = stemmer.stem_word(word)
    word = lemmatizer.lemmatize(word)
    return word

def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword."""
    accepted = bool(2 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted

def leaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.node=='NP'):
        yield subtree.leaves()

def get_terms(tree):
    for leaf in leaves(tree):
        term = [ normalise(word) for word, tag in leaf
            if acceptable_word(word) ]
        yield term
        


#=========================================================shared funtions

# check if a word is a stop word
def word_checking_stop(word, stop):
	if len(word) < 1:
		return 1
	elif word[0] in string.punctuation:
		return 2
	elif word[0].isdigit():
		return 3
	elif word in stop[0]: 
		return 4
	elif word in stop[1]: 
		return 5
	else:
		return 0


