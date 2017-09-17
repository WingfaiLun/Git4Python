'''
Created on 2017-09-10

@author: lockon
'''

import pymysql

# Get DB connection
def get_DB_conn():
    connection = pymysql.connect(
        host = 'gdufsjnu.mysql.rds.aliyuncs.com', 
        port = 3306, 
        user = 'dev', 
        passwd = '123456',
        db = 'pubmed',
        local_infile = 1,
        charset = 'utf8'
        )
    return connection