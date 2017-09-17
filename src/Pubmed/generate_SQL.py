'''
Created on 2017-09-10

@author: lockon
'''

import time, os
from Pubmed.extract_utils.fileutils import get_files_in_path, process_args
from Pubmed.extract_utils.logutils import ext_print

#Default path is the data folder, but it required absolute path when executing the SQL script
defaultFilePath = r'data'

#Generate the SQL scripts in a file for manual executing
def generate_SQL_File(fin, fout = None):
    if fout is None:
        fout = fin
    files = get_files_in_path(fin, 'csv')
    sql = ''
    for file in files:
        table = os.path.splitext(file)[0].split(os.path.sep)[1]
        if 'article' in table:
            sql += "LOAD DATA LOCAL INFILE '" + file + "' INTO TABLE " + table +  r" FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\"' LINES TERMINATED BY '\r\n';" + "\n"
        
    print(sql)
    f = open(os.path.join(fout, "LOAD_DATA.sql"), "w")
    f.write(sql)
    f.close()
     
      
if __name__ == '__main__' :
    print (ext_print('Start to Process'))
    start = time.clock()
    
    args = process_args(defaultFilePath, "")
    generate_SQL_File (args.i, args.o)
    
    end = time.clock()
    print(ext_print("Total cost time: " + str(end - start) + "s"))