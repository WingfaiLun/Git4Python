import pymysql

conn = pymysql.connect(
    host = 'gdufsjnu.mysql.rds.aliyuncs.com', 
    port = 3306, 
    user = 'dev', 
    passwd = '123456',
    db = 'gdufs_jnu'
    )

cur = conn.cursor()
executeResult = cur.execute("SELECT * FROM zq_target")
resultList = cur.fetchmany(executeResult)

print(executeResult)

for item in resultList:
    print(item)

cur.close()
conn.close()