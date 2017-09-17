'''
Created on 2017-09-09

@author: lockon
'''

import time
from Pubmed.extract_utils.fileutils import get_files_in_path, process_args
from Pubmed.extract_utils.logutils import ext_print
from Pubmed.extract_utils.dbutils import get_DB_conn

#default path is the data folder
defaultFilePath = r"..\data"

#Insert the article data by files, but the performance is bad, not recommend
def Insert_DB(fin):
    files = get_files_in_path(fin, 'csv')
    for file in files:
        print (ext_print("Processing file: " + file))
        sql = "LOAD DATA LOCAL INFILE '" + file + r"' INTO TABLE article_2014 FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\"' LINES TERMINATED BY '\r\n'"
        try:
            executeResult =  dbCur.execute(sql)
            print(executeResult)
        except Exception as e:
            print("Error occurs when executing SQL: " + str(e))
        conn.commit()
             
    print (ext_print('All tasks completed\n'))
    return True

if __name__ == '__main__':
    print (ext_print('Start to Process'))
    start = time.clock()
    
    conn  = get_DB_conn()
    dbCur = conn.cursor()
    
    args = process_args(defaultFilePath)
    Insert_DB(args.i)
    
    dbCur.close()
    conn.close() 

    end = time.clock()
    print(ext_print("Total cost time: " + str(end - start) + "s"))
    