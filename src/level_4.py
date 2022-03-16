from demo import callen,get_one_page
import requests
import re
import time
from bs4 import BeautifulSoup
import random

url='https://arxiv.org/list/cs.AI/'+str(20)+'?show=200'
html = get_one_page(url)
soup = BeautifulSoup(html, features='html.parser')
content = soup.dl
list_title = content.find_all('div', class_ = 'list-title mathjax')
titles=[]#收集标题的列表
for title in list_title:
        try:
            titles.append(title.text.split('Title: ', maxsplit=1)[1].split('\n')[0])
        except:
            continue
print('website complete')

for i in range(8,9):
    t=i+1
    url='http://8.130.18.34:8080/download/2020.%20'+str(t)+'.pdf'
    r = requests.get(url) 
    while r.status_code == 403:
            time.sleep(500 + random.uniform(0, 500))
            r = requests.get(url)
    paper_title=titles[i]
    pdfname = paper_title.replace("/", "_")   #pdf名中不能出现/和：
    pdfname = pdfname.replace("?", "_")
    pdfname = pdfname.replace("\"", "_")
    pdfname = pdfname.replace("*","_")
    pdfname = pdfname.replace(":","_")
    pdfname = pdfname.replace("\n","")
    pdfname = pdfname.replace("\r","")
    with open('D:/git_work1/Artificial Intelligence'+'/%s  %s.pdf'%(str(t),pdfname), "wb") as code:    
       code.write(r.content)
    print(t)