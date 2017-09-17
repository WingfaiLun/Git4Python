'''
Created on 2017-09-06
Extract elements form XML formatted trials
@author: lockon
'''

import os, time
import xml.etree.ElementTree as xml_parser
from Pubmed.extract_utils import fileutils
from Pubmed.extract_utils.logutils import ext_print

defaultFilePath = r'data' #Process files in the data folder

#=======================================================extract trial information from downloaded XML files
def CT_extractxml (fin, fout = None):
	if fout is None:
		fout = fin
	processed_list = [] # set processed trials into here to avoid redundancy
	
	files = fileutils.get_files_in_path(fin, 'xml')
	for file in files:
		if file in processed_list:
			continue
		print (ext_print ("Processing file: " + file))
		processed_list.append(file)
		if len(processed_list) % 1000 == 0:
			print (ext_print ('Processing  %d' % len(processed_list)))

		# read input data
		text = open(file, 'r', encoding='utf-8').read()
		if text is not None:
			ct_xml = xml_parser.fromstring(text)
			blocks = ct_xml.findall('MedlineCitation')
			ct_xml = ""
			for block in blocks:
				tempContent =  extract_component(block)
				pubDate = tempContent[2]
				if (pubDate is None or pubDate == ''):
					year = 0
				else: 
					year = int(pubDate)
				
				table = 'article_0-1950'
				if 2000 >= year >= 1951:
					table = 'article_1951-2000'
				elif 2005 >= year >= 2001:
					table = 'article_2001-2005'
				elif year > 2005:
					table = 'article_'+ str(year)
				else:
					table = 'article_unkown_year'
					
				outputFile = os.path.join(fout, table + ".csv")
				fileutils.write_csv_by_row(outputFile, tempContent)

	print (ext_print ('All tasks completed\n'))
	return True

def extract_component (block):
	PMID, JournalTitle, PubDate, ArticleTitle, Abstract, Keywords= '', '', '', '', [], []

	if block is not None:
		d = block.find ('PMID')
		if d is not None:
			PMID = d.text.strip()

		d = block.find('Article')
		if d is not None:
			e = d.find('Journal')
			if e is not None:
				# find PubDate
				f = e.find('JournalIssue')
				if f is not None:
					g = f.find('PubDate')
					if g is not None:
						h = g.find('Year')
						if h is not None:
							PubDate = h.text.strip()

				# find Journal_Title
				f = e.find('Title')
				if f is not None:
					JournalTitle = f.text.strip()

			# find ArticleTitle
			e = d.find('ArticleTitle')
			if e is not None:
				ArticleTitle = e.text.strip()

			# find Abstract
			e = d.find ('Abstract')
			if e is not None:
				f = e.findall ('AbstractText')
				for g in f:
					if g is not None and g.text is not None:
						j = None
						if "NlmCategory" in g.attrib:
							j = g.attrib["NlmCategory"]
						if j is None:
							Abstract.append(g.text.strip())
						else:
							Abstract.append(j.strip()+'='+g.text.strip())

		d = block.find('MeshHeadingList')
		if d is not None:
			e = d.findall('MeshHeading')
			for f in e:
				if f is not None:
					g = f.find('DescriptorName')
					if g is not None:
						Keywords.append(g.text.strip())
	return (PMID, JournalTitle, PubDate, ArticleTitle, Abstract, Keywords)

if __name__ == '__main__' :
	print (ext_print('Start to Process'))
	start = time.clock()
	
	args = fileutils.process_args(defaultFilePath)
	CT_extractxml (args.i, args.o)
	
	end = time.clock()
	print(ext_print("Total cost time: " + str(end - start) + "s"))