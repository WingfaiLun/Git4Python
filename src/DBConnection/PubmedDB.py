import pymysql

conn = pymysql.connect(
    host = 'gdufsjnu.mysql.rds.aliyuncs.com', 
    port = 3306, 
    user = 'dev', 
    passwd = '123456',
    db = 'pubmed',
    charset = 'utf8'
    )

cur = conn.cursor()
sql = "INSERT INTO article_2014 (`PMID`, `JournalTitle`, `PubDate`, `ArticleTitle`, `Abstract`, `Keywords`) VALUES ('20170909', 'JournalTitle', '2017', 'Adaptor protein GRB2 promotes Src tyrosine kinase activation and podosomal organization by protein-tyrosine phosphatase ϵ in osteoclasts.', 'Abstract', 'Keywords')";

executeResult = cur.execute(sql)
resultList = cur.fetchmany(executeResult)

print(executeResult)

conn.commit()

cur.close()
conn.close()