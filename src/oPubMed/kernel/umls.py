# class to store the umls maps
# @author: rm3086@columbia.edu
# @modified by: Tony HAO, th2510@columbia.edu


class UmlsDict:

	# constructor
	# @variable norm: map 'sentence' to 'preferred sentence'
	# @variable semantic: map 'preferred sentence' to 'semantic types'
	# @variable stype: list of semantic types 
	def __init__(self, udct, st):
			self.norm = {}
			self.semantic = {}
			self.stype = set()
			self.__load_from_file (udct, st)


	# load umsl data from files stored in 'dumls'
	def __load_from_file (self, udct, st):
		# load semantic types
		if st is not None:
			self.stype = set([c.lower() for c in st])
		else:
			self.stype = set()
		# load dictionary
		self.norm = {}
		self.semantic = {}
		if udct is not None:
			for u in udct:
				# semantic types
				stype = set (u[2].strip().split('|'))
				# preferred terms
				pterms = u[1].strip().split('|')
				ns = set ()
				for pt in pterms:
					ns.add (pt)
					sty = self.semantic.setdefault (pt, set())
					sty |= stype
					self.semantic[pt] = sty
				if len(ns) > 0:
					self.norm[u[0].strip()] = ns


	# set variables
	def set_normalizer (self,nm):
		self.norm = nm

	
	def set_semantic_map (self,smap):
		self.semantic_map = smap


	def set_semantic_type (self,stype):
		self.semantic_type = stype
		
		
	# retrieve the semantic type of a word
	@staticmethod
	def retrieve_semantic_type (t, umls):
		if umls is None:
			return None
		if t in umls.semantic:
			return sorted (umls.semantic[t])
		words = t.split()
		stype = set()
		for i in xrange(len(words)):
			for j in reversed(xrange(i+1, len(words)+1)):
				s = ' '.join (words[i:j])
				if s in umls.semantic:
					if (len(umls.stype) == 0) or (len(umls.semantic[s] & umls.stype) > 0):
						stype |= umls.semantic[s]
		if len(stype) == 0:
			return None
		return sorted(stype)
