# -*- encoding: utf-8 -*-
# Extract elements form XML formatted trials
# Created by Tony HAO, th2510@columbia.edu

import W_utility.file as ufile
from W_utility.log import ext_print
import xml.etree.ElementTree as xml_parser
import W_utility.web as web
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8');

#=======================================================extract trial information from downloaded xml files

def CT_extractxml (fin, fout=None):
	processed_list = [] # set processed trials into here to avoid redundency
	for root, dir, files in os.walk(fin):
		for f in files:
			if not f.endswith(".xml") or f in processed_list:
				continue
			print ext_print (f)
			processed_list.append(f)
			if len(processed_list)%1000 == 0:
				print ('Processing  %d' % len(processed_list))

			output = []
			# read input data
			fdin = os.path.join(root, f)
			text = ufile.read_file (fdin, 3, False)
			if text is not None:
				ct_xml = xml_parser.fromstring(text)
				blocks = ct_xml.findall('MedlineCitation')
				ct_xml = ""
				for block in blocks:
					(PMID, JournalTitle, PubDate, ArticleTitle, Abstract, Keywords) =  extract_component(block)
					output.append((PMID, JournalTitle, PubDate, ArticleTitle, Abstract, Keywords))
				blocks = []

			# set output data file
			fout = os.path.splitext(fdin)[0] + "_extracted.csv"

			ufile.write_csv (fout, output)
			print ext_print ('saved result in: %s' % fout)

	print ext_print ('all tasks completed\n')
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


# process and clean the eligibility criteria
def _process_ec_text (text):
	# handle special characters
 	text = text.strip().replace('\n\n', '#')
	text = text.replace ('\n', '')
	text = text.replace(u'＝','=').replace(u'＞', '>').replace(u'＜','<').replace(u'≤','<=').replace (u'≥','>=').replace(u'≦','<=').replace(u'≧','>=').replace(u'mm³','mm^3').replace(u'µl','ul').replace(u'µL','ul').replace(u'·','').replace(u'‐','-').replace(u'—','-')
	while '  ' in text:
		text = text.replace('  ',' ')
	text = text.encode('ascii', 'ignore')
	return text


# main function	

# processing the command line options
import argparse
def _process_args():
	parser = argparse.ArgumentParser(description='Downlaod all eligibility criteria from clinicaltrials.gov')
	# parser.add_argument('-i', default=r'E:\Datasets\Dataset_Medical\Dataset - PubMed\xml', help='file with the list of trials (default "./data/clinical-trials.csv"')
	parser.add_argument('-i', default=r'D:\Users\XML3', help='file with the list of trials (default "./data/clinical-trials.csv"')
	parser.add_argument('-o', default=None, help='output file; None: get default output path')
	return parser.parse_args(sys.argv[1:])


if __name__ == '__main__' :
	print ''
	args = _process_args()
	CT_extractxml (args.i, args.o)
	print ''
