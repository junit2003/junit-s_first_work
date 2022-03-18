import pymysql
import time
def searchword(keyword,db):
    cursor=db.cursor()
    sql='SELECT title from aipapers WHERE POSITION(\'%s\' IN title);'
    try:
        cursor.execute(sql%keyword)
        results=cursor.fetchall()
        if results==():
            print('Not Found')
        for result in results:
            print(result[0])
    except:
        print('Error')

def searchauthor(keyword,db):
    cursor=db.cursor()
    sql='SELECT * from aipapers WHERE POSITION(\'%s\' IN authors);'
    try:
        cursor.execute(sql%keyword)
        results=cursor.fetchall()
        if results==():
            print('Not Found')
        i=0
        for result in results:
            i+=1
            print('num '+str(i))
            print(result)
    except:
        print('Error')


def searchtime(keyword,db):
    cursor=db.cursor()
    sql='SELECT * from aipapers WHERE date=\'%s\';'
    try:
        cursor.execute(sql%keyword)
        results=cursor.fetchall()
        if results==():
            print('Not Found')
        i=0
        for result in results:
            i+=1
            print('num '+str(i))
            print(result)
    except:
        print('Error')

def searchyear(keyword,db):
    cursor=db.cursor()
    sql='SELECT * from aipapers WHERE POSITION(\'%s\' IN date);'
    try:
        cursor.execute(sql%keyword)
        results=cursor.fetchall()
        if results==():
            print('Not Found')
        i=0
        for result in results:
            i+=1
            print('num '+str(i))
            print(result)
    except:
        print('Error')


def main():
    db=pymysql.connect(host='localhost',user='root',password='76787678',port=3306,db='spiders')
    type=input("type:")
    k = input("keyword:")
    if type=='1':
        searchword(k,db)
    if type=='2':
        searchauthor(k,db)
    if type=='3':
        searchtime(k,db)
    if type=='4':
        searchyear(k,db)
    db.close()
    

if __name__ == '__main__':
    main()
    time.sleep(1)