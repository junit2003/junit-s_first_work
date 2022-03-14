from math import floor
import requests
import re
import time
import pandas as pd
from bs4 import BeautifulSoup
import pymysql
from collections import Counter
import os
import random
import smtplib
from smtplib import SMTP
from demo import get_one_page,read

#更新数据库
def callen():#找到文章总数
    url = 'https://arxiv.org/list/cs.AI/recent'
    html = get_one_page(url)
    soup = BeautifulSoup(html, features='html.parser')
    rec=soup.find('small')
    for sub in rec:
        num=re.findall(r"\d",sub.text)
        break
    sum=0
    for i in num:
        sum=sum*10
        sum+=int(i)
    return sum

def refdb(x,s,max,cursor,db):
    urlfin='https://arxiv.org/list/cs.AI/recent?show=2000'+x
    url='https://arxiv.org/list/cs.AI/recent?show=2000'
    html = get_one_page(url)
    soup = BeautifulSoup(html, features='html.parser')
    list_ids = soup.find_all('li')
    i=0
    for li in list_ids:
        i+=1
        num=li.find("a").get("href")
        if i>=2:
            break
    num=num.split('#item')[1]
    num=int(num)
    num-=1#最新一天的论文数量
    read(urlfin,s,num,cursor,db,22)


def main():
    db=pymysql.connect(host='localhost',user='root',password='76787678',port=3306,db='spiders')
    cursor=db.cursor()
    length=callen()
    for i in range(floor(length/2000)+1):
        if i==0:
            x=""
        else:
            x="&skip="+str(i*2000)
        refdb(x,i,length,cursor,db)


if __name__ == '__main__':
    main()
    time.sleep(1)
