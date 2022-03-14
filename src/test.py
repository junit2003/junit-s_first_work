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

#此处为做实验的文件，以防污染可以正式使用的代码
def get_one_page(url):
    response = requests.get(url)
    while response.status_code == 403:
        time.sleep(500 + random.uniform(0, 500))
        response = requests.get(url)
        print(response.status_code) 
    if response.status_code == 200:
        return response.text
    return None

def finddate(url):
    html = get_one_page(url)
    soup = BeautifulSoup(html, features='html.parser')
    date=soup.find(attrs={"name":"citation_online_date"})['content']
    return date

def read(x,s,max,cursor,db):
    url = 'https://arxiv.org/search/?searchtype=all&query=cs.AI&abstracts=show&size=200&order=-announced_date_first&date-date_type=submitted_date&start='+x
    html = get_one_page(url)
    soup = BeautifulSoup(html, features='html.parser')

    tag_ids = soup.find_all('p', class_="list-title is-inline-block")
    list_ids=[]#收集序号的列表
    for id in tag_ids:
        list_ids.append(id.text.split('\n')[0])
    tags_title = soup.find_all('p', class_="title is-5 mathjax")
    list_title=[]#收集标题的列表
    for title in tags_title:
        list_title.append(title.text.split('\n')[2].split('        ')[1])
    tags_authors = soup.find_all('p', class_="authors")
    list_authors=[]#收集作者的列表
    for authors in tags_authors:
        list_authors.append(authors.text.replace('\n', '').replace('             ','').replace('Authors:',''))
    list_subjects = soup.find_all('div', class_="tags is-inline-block")
    list_subject_split = []#收集领域的列表
    for subjects in list_subjects:
        subjects = subjects.text
        subjects = subjects.replace('\n\n', '')
        subjects = subjects.replace('\n', ' ')
        list_subject_split.append(subjects)
    tags_date=soup.find_all('p', class_="is-size-7")
    list_date=[]#收集提交日期的列表
    for date in tags_date:
        try:
            list_date.append(date.text.split('\n')[0].split('Submitted ')[1].split('; ')[0])
        except:
            continue
    for i in range(200):
        if list_subject_split[i].find('cs.AI')==-1:
            continue
        #strp=''
        sql='INSERT INTO aipapers(id,title,authors,date,tags,address) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'
        #strp+=list_ids[2]+list_title[2]+list_authors[2]+list_subject_split[2]+' '+list_date[2]
        if list_ids[i].find('cs')==-1:
            address='https://arxiv.org/pdf/'+list_ids[i].split('arXiv:')[1]
        else:
            id=list_ids[i].split('arXiv:cs/')[1]
            dt=''
            for i in range(4):
                dt.append(id[i])
            address='https://arxiv.org/ftp/cs/papers/'+dt+'/'+id+'.pdf'
        try:
            cursor.execute(sql%(list_ids[i],list_title[i],list_authors[i],list_subject_split[i],list_date[i],address))
            db.commit()
        except:
            db.rollback()
        #print(strp)
        #f.write(strp)
        print(s*1000+i+1)#输出记录了多少文件
        if s*1000+i+1==max:#输出完了就停止
            break
    print("completed")

def callen():#找到文章总数
    url = 'https://arxiv.org/search/?searchtype=all&query=cs.AI&abstracts=show&size=200&order=-announced_date_first&date-date_type=submitted_date&start=0'
    html = get_one_page(url)
    soup = BeautifulSoup(html, features='html.parser')
    rec=soup.find('h1', class_="title is-clearfix")
    rec=(rec.text.split('of ')[1].split(' result')[0].split(','))
    sum=0
    for num in rec:
        sum*=1000
        sum+=int(num)
    return sum


def download(paper_id,paper_title):
    r = requests.get('https://arxiv.org/pdf/' + paper_id) 
    while r.status_code == 403:
        time.sleep(500 + random.uniform(0, 500))
        r = requests.get('https://arxiv.org/pdf/' + paper_id)
    print(r.status_code)
    paper_id = paper_id.split('arXiv:',maxsplit=1)[1]
    pdfname = paper_title.replace("/", "_")   #pdf名中不能出现/和：
    pdfname = pdfname.replace("?", "_")
    pdfname = pdfname.replace("\"", "_")
    pdfname = pdfname.replace("*","_")
    pdfname = pdfname.replace(":","_")
    pdfname = pdfname.replace("\n","")
    pdfname = pdfname.replace("\r","")
    print('D:/git_work1/Artificial Intelligence'+'/%s %s.pdf'%(paper_id, paper_title))
    with open('D:/git_work1/Artificial Intelligence'+'/%s %s.pdf'%(paper_id,pdfname), "wb") as code:    
       code.write(r.content)

def acq(subject):
    str=''
    flag=0
    for c in subject:
        if c=='(':
            flag=1
            continue
        if c==')':
            break
        if flag==1:
            str+=c
    return str

def main():
    db=pymysql.connect(host='localhost',user='root',password='76787678',port=3306,db='spiders')
    cursor=db.cursor()
    length=callen()
    #f = open("out.txt","w",encoding='utf-8') 
    for i in range(floor(length/200)+1):
        if i==0:
            x=""
        else:
            x=i*200
        read(str(x),i,length,cursor,db)
    db.close()


if __name__ == '__main__':
    main()
    time.sleep(1)

