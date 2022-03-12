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

def read(x,s,max):
    f = open("out.txt","w",encoding='utf-8')  
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
    for i in range(1000):
        strp='\n\nid: '+list_ids[i].text+'\n'+list_title[i].text.split('\n', maxsplit=2)[1]+list_authors[i].text+'tag: '        
        for subject in list_subject_split[i]:
            strp=strp+subject+' '
        url='https://arxiv.org/abs/'+list_ids[i].text.split('arXiv:',maxsplit=1)[1]
        #date=finddate(url)
        #strp=strp+'\ndate: '+date
        f.write(strp)
        print(s*1000+i+1)#输出记录了多少文件
        if s*1000+i+1==max:#输出完了就停止
            break

def callen():
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
def main():
    length=callen()
    for i in range(floor(length/1000)+1):
        if i==0:
            x=""
        else:
            x="&skip="+str(i*1000)
        read(x,i,length)

if __name__ == '__main__':
    main()
    time.sleep(1)
