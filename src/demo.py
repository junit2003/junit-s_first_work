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

def read(url,s,max,cursor,db,y):#存储搜到的记录url是访问的网页，s是访问第几次，max是最多几个
    html = get_one_page(url)
    soup = BeautifulSoup(html, features='html.parser')
    content = soup.dl
    list_ids = content.find_all('a', title = 'Abstract')
    list_title = content.find_all('div', class_ = 'list-title mathjax')
    list_authors = content.find_all('div', class_ = 'list-authors')
    list_subjects = content.find_all('div', class_ = 'list-subjects')
    list_subject_split = []#收集领域的列表
    for subjects in list_subjects:
        subs=''
        subjects = subjects.text.split(': ', maxsplit=1)[1]
        subjects = subjects.replace('\n\n', '')
        subjects = subjects.replace('\n', '')
        subject_split = subjects.split('; ')
        try:
            for subject in subject_split:
                subs+=subject+' '
            list_subject_split.append(subs)
        except:
            continue
    ids=[]#收集序号的列表
    for id in list_ids:
        try:
            ids.append(id.text)
        except:
            continue
    titles=[]#收集标题的列表
    for title in list_title:
        try:
            titles.append(title.text.split('Title: ', maxsplit=1)[1].split('\n')[0])
        except:
            continue
    l_authors=[]#收集作者的列表
    for l_au in list_authors:
        authors=''
        for author in l_au.text.split('\n'):
            if author !='' and author!='Authors:':
                authors+=author
        try:
            l_authors.append(authors)
        except:
            continue
    for i in range(2000):
        sql='REPLACE INTO aipapers(id,title,authors,date,tags,address) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'
        #strp='\n\nid: '+list_ids[i].text+'\n'+list_title[i].text.split('\n', maxsplit=2)[1]+list_authors[i].text+'tag: '
        try:
            if ids[i].find('cs')==-1:
                dt=ids[i].split('arXiv:')[1]
                address='https://arxiv.org/pdf/'+dt
            else:
                try:
                    id=ids[i].split('arXiv:cs/')[1]
                except:
                    print(s*2000+i+1)
                    continue
                dt=''
                for j in range(4):
                    dt+=(id[j])
                address='https://arxiv.org/pdf/cs/'+id+'.pdf'
        except:
            print(str(y)+'error')
            print(s*2000+i+1)
            break
        date='19'
        for j in range(2):
            date+=dt[j]
        date+='/'
        for j in range (2,4):
            date+=dt[j]
        try:
            cursor.execute(sql%(ids[i],titles[i],l_authors[i],date,list_subject_split[i],address))
            db.commit()
        except:
            db.rollback()
        #strp=strp+'\ndate: '+date
        #f.write(strp)
        #download(list_ids[i].text,list_title[i].text.split('\n', maxsplit=2)[1])
        if s*2000+i+1==max:#输出完了就停止
            print(str(y)+" completed")
            break


def callen(y):#找到文章总数
    if y<10:
        url = 'https://arxiv.org/list/cs.AI/0'+str(y)+'?show=10'
    else:
        url = 'https://arxiv.org/list/cs.AI/'+str(y)+'?show=10'
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


def download(y,x,n,s):#y是年份，n是下载几份
    url = 'https://arxiv.org/list/cs.AI/'+str(y)+'?show=1000'+x
    html = get_one_page(url)
    soup = BeautifulSoup(html, features='html.parser')
    content = soup.dl
    list_ids = content.find_all('a', title = 'Abstract')
    list_title = content.find_all('div', class_ = 'list-title mathjax')
    for i in range(n):
        (paper_id,paper_title)=(list_ids[i].text,list_title[i].text.split('\n', maxsplit=2)[1])
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
        print(s*2000+i+1)

def acq(subject):#提取领域
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
    #f = open("out.txt","w",encoding='utf-8') 
    for y in range(12,23):
        length=callen(y)
        for i in range(floor(length/2000)+1):
            if i==0:
                x=""
            else:
                x="&skip="+str(i*2000)
            if y<10:
                url = 'https://arxiv.org/list/cs.AI/0'+str(y)+'?show=2000'+x
            else:
                url = 'https://arxiv.org/list/cs.AI/'+str(y)+'?show=2000'+x
            read(url,i,length,cursor,db,y)
    db.close()


if __name__ == '__main__':
    main()
    time.sleep(1)
