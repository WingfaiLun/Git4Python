'''
Created on 2017-09-09

@author: lockon
'''

import time
from Pubmed.extract_utils.dbutils import get_DB_conn
from Pubmed.extract_utils.logutils import ext_print

#Find all the articles by year, the default year is 2014
def query_articles_by_year(year = '2014'):
    conn = get_DB_conn()
    cur = conn.cursor()
    executeResult = cur.execute("SELECT * FROM article_" + year)
    resultList = cur.fetchmany(executeResult)
    cur.close()
    conn.close() 
    return resultList

if __name__ == '__main__':
    print (ext_print('Start to Process'))
    start = time.clock()
    
    articles = query_articles_by_year('2014')
    for item in articles:
        print(item)

    end = time.clock()
    print(ext_print("Total cost time: " + str(end - start) + "s"))