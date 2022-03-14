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
from demo import get_one_page, read ,callen
#进行下载
def main():
    
    y=input('year:')
    length=callen(y)
    n=input('份数(全部下载请输入-1):')
    y=int(y)
    n=int(n)
    if n==-1:
        length=length
    elif int(n)<length:
        length=n
    else:
        length=length
    l=length
    for i in range(floor(length/1000)+1):
        if i==0:
            x=""
        else:
            x="&skip="+str(i*1000)
        if l>=1000:
            l-=1000
            download(y,x,1000,i)
        else:
            download(y,x,l,i)

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
