# -*- encoding: utf-8 -*-
# Kernel algorithm of CST mining
# Created by Tony HAO, th2510@columbia.edu

import kernel_mining
import c_value
import string, math, re
from umls import UmlsDict
from compiler.ast import Break
from nltk.inference.tableau import Categories
from NLP.porter2 import stem


# Kernel algorithm of CST mining
#===================================================N-gram -based mining
def mining_CST_ngram (docs, ngr = 8, jonce = False, stop = None, use_dumls = False, umls = None, use_pos = True, ptag = None, prule = None, use_stem = False, textsection = 'all', split = None, fre_th = 0, c_value_th = 0, stmethod=0, all_pos_tags=None):
	
	# generate phrases from a set of documents
	unique_match_ngrams, unique_unmatch_ngrams, original_ngrams, standardized_ngrams = {},{},{},{}
	for i in xrange(len(docs)):
 		if i%1000 == 0: # output progress
 			print ('processing %d' % i)
 		text = preprocessing(docs[i])
		text = split_text_inclusion_exclusion(text, textsection)
 		doc_ngrams = kernel_mining.Generate_ngrams_document (text, ngr, stop, use_pos, ptag, use_stem, split, all_pos_tags)

		# standardize ngrams
		local_processed = {}
		for key, value in doc_ngrams.iteritems():
			count = 1 if (jonce) else value # record the occurrence as once or not

			mapped_concept = ""
			if use_dumls: # use UMLS or not
				if key in standardized_ngrams:
					mapped_concept = standardized_ngrams[key]
				else:
					mapped_concept = standardizing (key.split(), umls, stop)
					if mapped_concept is not None and kernel_mining.word_checking_stop(mapped_concept, stop) ==0:
						standardized_ngrams[key] = mapped_concept
					else:
						mapped_concept = ""
					
			if mapped_concept != "": # if map UMLS
				if mapped_concept not in local_processed: # not proceed in current doc so can be added into unique_match_ngrams
					if mapped_concept in unique_match_ngrams: # record mapped ngrams
						unique_match_ngrams[mapped_concept] += count
					else:
						unique_match_ngrams[mapped_concept] = count
					local_processed[mapped_concept]=True
				if mapped_concept in original_ngrams: # record original ngrams
					if key in original_ngrams[mapped_concept]: 
						original_ngrams[mapped_concept][key] += count 
					else:
						original_ngrams[mapped_concept][key] = count
				else:
					original_ngrams[mapped_concept] = {key:count}
			else:
				if key in unique_unmatch_ngrams: # record unmapped ngrams
					unique_unmatch_ngrams[key] += count
				else:
					unique_unmatch_ngrams[key] = count
	
	# get frequent n-grams by threshold comparison
	fre_match_ngrams = kernel_mining.Get_frequent_ngrams (unique_match_ngrams, (float(fre_th) * len(docs)))
	fre_unmatch_ngrams = kernel_mining.Get_frequent_ngrams (unique_unmatch_ngrams, (float(fre_th) * len(docs)))

 	# apply C-value to filter sub-strings that usually occurred in sup-strings
 	fre_match_ngrams = c_value.C_value_filtering  (fre_match_ngrams, c_value_th, stop)
 	fre_unmatch_ngrams = c_value.C_value_filtering (fre_unmatch_ngrams, c_value_th, stop)
	
	# extract semantic type
	cdes = {}
 	for key, value in fre_match_ngrams.iteritems():
 		pre_st = ''		
		if key in cdes:  
			cdes[key][0] += value # record final frequency value
		else:
			pre_st = UmlsDict.retrieve_semantic_type(key,umls) # get semantic types from UMLS, calculate only once for each CST
			if pre_st is not None:
	 			if (stmethod == 1):	# output first semantic types
	 				pre_st = pre_st[0]
	 			elif (stmethod == 2):# extract types according to preference semantic rules
 					for stype in pre_st:
 						if stype in prule:
 							pre_st = stype
 							break					
			cdes[key] = [value, original_ngrams[key], pre_st]

 	return 	(cdes, fre_match_ngrams, fre_unmatch_ngrams) 
  


#===================================================Syntatic tree -based mining

def mining_CST_syntatic (docs, jonce = False, stop = None, use_dumls = False, umls = None, textsection = 'all', split = None, fre_th = 0, stmethod=0, all_pos_tags=None):
	
	# generate phrases from a set of documents
	unique_match_ngrams, unique_unmatch_ngrams, original_ngrams, standardized_ngrams = {},{},{},{}
	for i in xrange(len(docs)):
 		if i%1000 == 0: # output progress
 			print ('processing %d' % i)
		
		text = preprocessing(docs[i])
		text = split_text_inclusion_exclusion(text, textsection)

		doc_ngrams = kernel_mining.Extract_phrases_document (text, stop, split, all_pos_tags)

		# standardize ngrams
		local_processed = {}
		for key, value in doc_ngrams.iteritems():
			count = 1 if (jonce) else value # record the occurrence as once or not

			mapped_concept = ""
			if use_dumls: # use UMLS or not
				if key in standardized_ngrams:
					mapped_concept = standardized_ngrams[key]
				else:
					mapped_concept = standardizing (key.split(' '), umls, stop)
					if mapped_concept is not None and kernel_mining.word_checking_stop(mapped_concept, stop) ==0:
						standardized_ngrams[key] = mapped_concept
					else:
						mapped_concept = ""
					
			if mapped_concept != "": # if map UMLS
				if mapped_concept not in local_processed: # not proceed in current doc so can be added into unique_match_ngrams
					if mapped_concept in unique_match_ngrams: # record mapped ngrams
						unique_match_ngrams[mapped_concept] += count
					else:
						unique_match_ngrams[mapped_concept] = count
					local_processed[mapped_concept]=True
				if mapped_concept in original_ngrams: # record original ngrams
					if key in original_ngrams[mapped_concept]: 
						original_ngrams[mapped_concept][key] += count 
					else:
						original_ngrams[mapped_concept][key] = count
				else:
					original_ngrams[mapped_concept] = {key:count}
			else:
				if key in unique_unmatch_ngrams: # record unmapped ngrams
					unique_unmatch_ngrams[key] += count
				else:
					unique_unmatch_ngrams[key] = count
		
	# get frequent n-grams by threshold comparison
	fre_match_ngrams = kernel_mining.Get_frequent_ngrams (unique_match_ngrams, (float(fre_th) * len(docs)))
	fre_unmatch_ngrams = kernel_mining.Get_frequent_ngrams (unique_unmatch_ngrams, (float(fre_th) * len(docs)))

			
	# extract semantic type
	cdes = {}
 	for key, value in fre_match_ngrams.iteritems():
 		pre_st = ''		
		if key in cdes:  
			cdes[key][0] += value # record final frequency value
		else:
			pre_st = UmlsDict.retrieve_semantic_type(key,umls) # get semantic types from UMLS, calculate only once for each CST
			if pre_st is not None:
	 			if (stmethod == 1):	# output first semantic types
	 				pre_st = pre_st[0]
	 			elif (stmethod == 2):# extract types according to preference semantic rules
 					for stype in pre_st:
 						if stype in prule:
 							pre_st = stype
 							break					
			cdes[key] = [value, original_ngrams[key], pre_st]

 	return 	(cdes, fre_match_ngrams, fre_unmatch_ngrams) 


#============================other functions

def preprocessing (text):
    while '  ' in text:
        text = text.replace('  ',' ')
    return text.lower()


def split_text_inclusion_exclusion(otext, textsection):
	if textsection =='all':
		return otext
	else:
		in_fea = 'inclusion criteria:|inclusion:|inclusion criteria\W\W|inclusion for'
		ex_fea = 'exclusion criteria:|exclusion:|exclusion criteria\W\W|exclusion for'
		in_text, ex_text = '', ''
		in_bool = True
		
		text = otext.lower()
		while text != '':
			if in_bool:
				n_pos = re.search('('+ex_fea+')',text)
				if n_pos is not None:
					in_text += text[0:n_pos.start()]
					text = text[n_pos.start():]
				else:
					in_text += text[0:]
					text = ''
				in_bool = False
			else:
				n_pos = re.search('('+in_fea+')',text)
				if n_pos is not None:
					ex_text += text[0:n_pos.start()]
					text = text[n_pos.start():]
				else:
					ex_text += text[0:]
					text = ''
				in_bool = True
		
		if textsection =='inclusion': 
			return in_text 
		else:
			return ex_text


# standardize text by umls dictionary, umls semantic categories, and english stemmer (optional)
def standardizing (words, umls, stop):
	eng = False
	# map to umls
	if umls is not None:
		pwords = []
		status = []
		i = 0
		while i < len(words):
			fnd = False
			if kernel_mining.word_checking_stop(words[i], stop) in [5,0]: # judge stop word
				for j in reversed(xrange(i+1, len(words)+1)):
					if kernel_mining.word_checking_stop(words[j-1], stop) in [5,0]:  # judge stop word
						s = ' '.join (words[i:j])
						if (s in umls.norm): # another filter is "and (len(umls.norm[s]) <= 10)"
							cl = int(50)
							fs = None
							for pt in umls.norm[s]:
								dpt = pt.decode('utf-8')
								# retain same
								if dpt == s.decode('utf-8'):
									fs = s.decode('utf-8')
									break
								# acronym
								if len(umls.norm[s]) > 1:
									tkn = dpt.split()
									if len(tkn) == len(s):
										init = set(s)
										acr = len(tkn)
										for t in tkn:
											if t[0] in init:
												acr -= 1
										if acr == 0:
											fs = dpt
											break
								# retain shorter
								if (len(dpt) < cl):
									fs = dpt
									cl = len(dpt)
							s = fs
						if s in umls.semantic:
							if (len(umls.stype) == 0) or (len(umls.semantic[s] & umls.stype) > 0):
								pwords.append (s.encode('utf-8'))
								status.append (True)
								fnd = True
 								i = j
 								continue # do not stop the iterations to get subsets
			if fnd is False:
				pwords.append(words[i])
				status.append(False)
				i += 1
		# not found any umls term, ngram not valid
		if True not in status:
			return None 
		# english stemmer
		if eng is True:
			for i in xrange(len(pwords)):
				if status[i] is False:
					pwords[i] = stem(pwords[i])
		# processing repetition
		uwords = set (pwords)
		if len(uwords) <= math.floor(len(pwords)/float(2)):
			return None
		return ' '.join(pwords)
	elif eng is True:
		# english only
		return ' '.join(__english_stemming(words))
	else:
		# nothing to do
		return ' '.join(words)


# english stemming
def __english_stemming (words):
	for i in xrange(len(words)):
		words[i] = stem(words[i])
	return words
	

# Load UMLS so that call easily
# dict: list; stype: set;
def Load_UMLS (dict, stype):
	return UmlsDict (dict, stype)
