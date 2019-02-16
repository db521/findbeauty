# coding=utf-8
import os
import re
import threading
import time

import requests
import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()
cookies = {
    'cookies': '__cfduid=d1a50478a43f118736847d328be2cceab1548462867; PHPSESSID=qaq1nm25g35htamas6ho64uot3; kt_tcookie=1;'
               ' kt_is_visited=1; kt_ips=118.26.142.83%2C97.64.24.79; __asc=18766a7b1688794bd51aa5ed3ed; __auc=18766a7b1688794bd51aa5ed3ed;'
               ' _ga=GA1.2.1831337609.1548462899; _gid=GA1.2.835901396.1548462899; _ym_uid=1548462899440317366; _ym_d=1548462899; _ym_isad=1;'
               ' splashWeb-645543-42=1; nb-no-req-645543=true; visitCount=7; tcout_c=1;'
               'video_log=pregnant-massage%3A1548462957%3Bvoyeur-sat01429%3A1548463930%3Bhidden-aged-wife-massage'
               '%3A1548464028%3Bhidden-web-camera-clinic-in-massage-room-two-hidden-camera-in-clinic-massage-room-47-03'
               '%3A1548464093%3B; kt_qparams=dir%3Dvoyeur-sat01429; __atuvc=10%7C4; __atuvs=5c4bab665c9c3daa009; '
               '_gat_UA-7940408-49=1; _gat=1; _gat_UA-51278971-1=1'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/69.0.3497.81 Safari/537.36'}
proxies = {'https': 'https://127.0.0.1:1080'}
origin = 'https://voyeurhit.com/'
path = './mp4/'


def newT():
    all = c.execute('select download_url from video_url where download_url not null').fetchall()
    for x in all:
        with open('ab.txt','a+') as f:
            print(x[0],file=f)

newT()
