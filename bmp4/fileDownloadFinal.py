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
path = 'g:/mp4/'


def downloadfile(urlAndfile):
    for x in urlAndfile:


        file_name = filename + '.mp4'
        if not os.path.exists(path + file_name):
            r1 = requests.get(url, proxies=proxies, cookies=cookies, headers=headers)
            if r1.status_code == 200:
                file1 = r1.content
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':开始写入文件：：', path + file_name)
                with open(path + file_name, 'wb') as file_text:
                    file_text.write(file1)
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':写入成功!文件为：：', path + file_name)
            else:
                with open('error.log', 'a+') as f1:
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '请求url有问题，不能下载', url, filename,r1.status_code, file=f1)
        else:
            print(file_name + '文件已经存在了，继续下载下一个')


# 启动线程的数量
def newT():
    all = c.execute('select v.access_url,d.download_url from videos v,dload d where v.video_id=d.video_id').fetchall()
    num_proc = 20
    equal_mount_job=[all[x:x+num_proc] for x in range(0,len(all),num_proc)]# 按照线程数量平均分配到每个线程基本相同的活
    thread_list = list()
    for i in range(num_proc):
        t = threading.Thread(target=downloadfile, args=(equal_mount_job[i],))  # 平均分配后的一个列表传给下载函数
        thread_list.append(t)

    for t in thread_list:
        t.start()


newT()
