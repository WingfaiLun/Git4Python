'''
Created on 2017-09-09

@author: lockon
'''

import csv, time
from Pubmed.extract_utils.fileutils import get_files_in_path, process_args
from Pubmed.extract_utils.logutils import ext_print
from Pubmed.extract_utils.dbutils import get_DB_conn

defaultFilePath = r'..\data'

def Insert_DB(fin):
    files = get_files_in_path(fin, 'csv')
    print(files)
    for file in files:
        print (ext_print("Processing file: " + file))

        # read input data
        rows = csv.reader(open(file, 'r', encoding='utf-8'))
        for row in rows:
            pubDate = row[2]
            if pubDate != '2014':  # To split tasks into differnt machines with MySQL, process tables separatly
                continue
            table = "article_" + pubDate

            # if (row[2] == '' or row[2] is None): PubDate = 0
            # PubDate = int(PubDate)
            # table = 'article_0-1950'
            # if 2000 >= PubDate >= 1951:
            #     table = 'article_1951-2000'
            # if 2005 >= PubDate >= 2001:
            #     table = 'article_2001-2005'
            # elif PubDate > 2005:
            #     table = 'article_'+ str(PubDate)
            
            param = (row[0], row[1], pubDate, row[3], row[4], row[5])
            sql = "INSERT INTO `" + table + "` (`PMID`, `JournalTitle`, `PubDate`, `ArticleTitle`, `Abstract`, `Keywords`) VALUES(%s, %s, %s, %s, %s, %s);"
            try:
                dbCur.execute(sql, param)
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
    