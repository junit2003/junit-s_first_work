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
    url = 'https://arxiv.org/list/cs.AI/22?show=1000'+x
    html = get_one_page(url)
    soup = BeautifulSoup(html, features='html.parser')
    content = soup.dl
    list_ids = content.find_all('a', title = 'Abstract')
    list_title = content.find_all('div', class_ = 'list-title mathjax')
    list_authors = content.find_all('div', class_ = 'list-authors')
    list_subjects = content.find_all('div', class_ = 'list-subjects')
    list_subject_split = []
    for subjects in list_subjects:
        subjects = subjects.text.split(': ', maxsplit=1)[1]
        subjects = subjects.replace('\n\n', '')
        subjects = subjects.replace('\n', '')
        subject_split = subjects.split('; ')
        list_subject_split.append(subject_split)
    for i in range(3):
        sql='INSERT INTO aipapers(id,title,authors,date,tags,address) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'
        strp='\n\nid: '+list_ids[i].text+'\n'+list_title[i].text.split('\n', maxsplit=2)[1]+list_authors[i].text+'tag: '
        tags=''        
        for subject in list_subject_split[i]:
            strp=strp+subject+' '
            tags+=acq(subject)+' '
        title=list_title[i].text.split('Title: ', maxsplit=1)[1]
        title=title.split('\n')[0]
        authors=''
        for author in list_authors[i].text.split('\n'):
            if author !='' and author!='Authors:':
                authors+=author
        url='https://arxiv.org/abs/'+list_ids[i].text.split('arXiv:',maxsplit=1)[1]
        date=finddate(url)
        try:
            cursor.execute(sql%(list_ids[i].text,title,authors,date,tags,url))
            db.commit()
        except:
            db.rollback()
        #strp=strp+'\ndate: '+date
        #f.write(strp)
        #download(list_ids[i].text,list_title[i].text.split('\n', maxsplit=2)[1])
        print(s*1000+i+1)#输出记录了多少文件
        if s*1000+i+1==max:#输出完了就停止
            break
    print("completed")

def callen():#找到文章总数
    url = 'https://arxiv.org/list/cs.AI/22?show=10'
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
    length=0
    #f = open("out.txt","w",encoding='utf-8') 
    for i in range(floor(length/1000)+1):
        if i==0:
            x=""
        else:
            x="&skip="+str(i*1000)
        read(x,i,length,cursor,db)
    db.close()


if __name__ == '__main__':
    main()
    time.sleep(1)

