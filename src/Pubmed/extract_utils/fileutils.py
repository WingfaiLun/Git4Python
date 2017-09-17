'''
Created on 2017-09-10

@author: lockon
'''
import argparse, os, csv, sys
from Pubmed.extract_utils.logutils import strd_logger

defaultInputPath = r'data'
log = strd_logger('myLogger')

# processing the command line options
def process_args(inputPath = defaultInputPath, outputPath = None):
    parser = argparse.ArgumentParser(description = 'Download all eligibility criteria from clinicaltrials.gov')
    parser.add_argument('-i', default = inputPath, help = 'file path with the list of trials (default path is "./data/')
    parser.add_argument('-o', default = outputPath, help = 'output file; None: get default output path')
    return parser.parse_args(sys.argv[1:])

# Get files in the path with expanded name
def get_files_in_path(path, expandedName = ''):
    fileList = []
    for root, dir, files in os.walk(path):
        for f in files:
            if expandedName is not None:
                if f.lower().endswith("." + expandedName):
                    fdin = os.path.join(root, f)
                    fileList.append(fdin)
    return fileList

# write data in format of [(x1,y1,z1),(x2,y2,z2)] to a csv file
def write_csv (filename, data, logout = True):
    try:
        doc = csv.writer (open(filename, 'w', encoding='utf-8', newline=''), delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for d in data:
            doc.writerow (d)
    except Exception as e:
        if logout is True:
            log.error(e)

#wrtie data to csv file for one row            
def write_csv_by_row (filename, data, logout = True):
    try:
        doc = csv.writer (open(filename, 'a', encoding='utf-8', newline=''), delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        doc.writerow (data)
    except Exception as e:
        if logout is True:
            log.error(e)

# process and clean the eligibility criteria
def process_ec_text (text):
    text = text.strip().replace('\n\n', '#')
    text = text.replace ('\n', '')
    text = text.replace(u'＝','=').replace(u'＞', '>').replace(u'＜','<').replace(u'≤','<=').replace (u'≥','>=').replace(u'≦','<=').replace(u'≧','>=').replace(u'mm³','mm^3').replace(u'µl','ul').replace(u'µL','ul').replace(u'·','').replace(u'‐','-').replace(u'—','-')
    while '  ' in text:
        text = text.replace('  ',' ')
    text = text.encode('ascii', 'ignore')
    return text