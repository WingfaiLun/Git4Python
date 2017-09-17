# filter words by C-value calculation, train threshold
# Created by Tony HAO, th2510@columbia.edu

from kernel_mining import word_checking_stop
import re, math
from itertools import groupby


# calculate c_value using <Automatic Recognition of Multi-Word Terms: the C-value/NC-value Method> by Katerina Frantzi, et, al.
def C_value_calculating(str, freq, has_long=False, long_freq=None, long_num=None):
	ln = len(str.split())
	if ln == 0:
		return 
	if ln == 1: # the c-value for a single word is 0
		ln += 0.1
	if has_long and long_num > 0:
		fr = freq - (long_freq/float(long_num))
		cval = math.log (ln, 2) * fr # log2|a|*(f(a)-f(b))
	else:
		cval = math.log (ln, 2) * freq # log2|a|*f(a)
		
	return cval



# filter substring according to c-value coefficient
def _multi_word_filtering (tags):
	# count term frequency	
	ctags = tags
	# iterate sorting by tagsure length and frequency
	substr = {}
	cval = {}
	stags = [(k,v) for k,v in reversed(sorted(ctags.iteritems(), key = lambda x:len(x[0].split())))]
	for k,gr in groupby(stags, lambda x:len(x[0].split())):
		for sf in reversed(sorted (gr, key = lambda x:x[1])):
			# compute c-value	
			if sf[0] not in substr:
				cval[sf[0]] = sf[1] * math.log (len(sf[0].split()), 2)
			else:
				fr = sf[1] - (substr[sf[0]][1]/float(substr[sf[0]][2]))
				ln = len(sf[0].split())
				if ln == 1:
					ln += 0.1
				cval[sf[0]] = math.log (ln, 2) * fr
			# process substrings
			tk = sf[0].split ()
			for i in xrange(len(tk)):
				for j in xrange(i+1, len(tk)+1):
					sub = ' '.join (tk[i:j])
					if (sub != sf[0]) and (sub in ctags):
						val = substr.setdefault (sub, (ctags[sub], 0, 0))				
						upd = sf[1]
						if sf[0] in substr:
							upd -= substr[sf[0]][1]
						substr[sub] = (val[0], val[1] + upd, val[2]+1)
	# filter substrings
	for f in tags.keys():
		sstr = f[max(0,f.find(':')+1):]
		if (sstr in substr) and (cval[sstr] < 0.1):
			del tags[f]
	return tags

# filter substring according to c-value coefficient
# modified from rm3086@columbia.edu
# Note: after fully consideration, C-value filtering cannot be used before UMLS mapping since it may filter something that can be used for mapping.
# parameters: words (a word dictionary)
def C_value_filtering (words, threshold, stop):
	cwords = words
	substr = {} # all substring
	cval = {} # all c_value

	# iterate sorting by word length and frequency
	cwords = [(k,v) for k,v in reversed(sorted(cwords.iteritems(), key = lambda x:len(x[0].split())))]
	for k,gr in groupby(cwords, lambda x:len(x[0].split())): # round by round according to their length
		for sf in reversed(sorted (gr, key = lambda x:x[1])):
			# compute c-value	
			if sf[0] not in substr:
				cval[sf[0]] =  C_value_calculating(sf[0], sf[1])
			else:
				cval[sf[0]] =  C_value_calculating(sf[0], sf[1], True, substr[sf[0]][0], substr[sf[0]][1])
			# process substrings
			tk = sf[0].split ()

# 			stop_pos = [] # record all positions of stop words in the phrase to increase efficiency
# 			for i in xrange(len(tk)):
# 				if 4 > word_checking_stop(tk[i], stop) > 0:
# 					stop_pos.append(i)				

			for i in xrange(len(tk)):
# 				if i in stop_pos:
# 					continue
				for j in xrange(i+1, len(tk)+1):
# 					if (j-1) in stop_pos:# check validity
# 						continue
					sub = ' '.join (tk[i:j])
					if (sub != sf[0]) and (sub in words):
						val = substr.setdefault (sub, (0, 0))				
						upd = sf[1]
						if sf[0] in substr:
							upd -= substr[sf[0]][1] # it has been considered
						substr[sub] = (val[0] + upd, val[1]+1)
						
	# filter substrings
	for f in words.keys():
		sstr = f[max(0,f.find(':')+1):]
		if (sstr in substr) and (cval[sstr] < threshold):
			del words[f]
			
	return words


# train to get best threshold by calculating maximum C-value
# parameters: texts (a list of text);  del_words_arr (a list of words in the format of "First|longer str1|longer str2"); return a float value
def C_value_threshold_training (texts, del_words_arr):
	cval_max = 0
	for del_words in del_words_arr:
		words = del_words.split('|')
		freq, freq_long = 0, 0
		for i in xrange(len(words)):
			r = re.compile(r'[^\w\d]'+words[i]+'[^\w\d]', re.IGNORECASE)
			for text in texts:
				text = ' ' + text + ' '
				if i == 0: # first, used as short string for training
					freq += len(r.findall(text))
				else:
					freq_long += len(r.findall(text))
		if len(words) > 1:
			cval =  C_value_calculating(words[0], freq, True, freq_long, len(words)-1)
		else:
			cval =  C_value_calculating(words[0], freq)
			
		cval_max = max(cval, cval_max)

	return cval_max