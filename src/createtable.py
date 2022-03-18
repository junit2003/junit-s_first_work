import pymysql
#建表

db=pymysql.connect(host='localhost',user='root',password='',port=3306,db='spiders')
cursor=db.cursor()
sql='CREATE TABLE IF NOT EXISTS aipapers(id VARCHAR(255),title VARCHAR(5000),authors VARCHAR(1000),date VARCHAR(255),tags VARCHAR(500),address VARCHAR(500), PRIMARY KEY (id))'
cursor.execute(sql)
print("completed")
db.close()