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
from demo import download, read ,callen
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