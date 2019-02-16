# encoding: utf-8
import threading
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import sqlite3

conn = sqlite3.connect('test.db', check_same_thread=False)
c = conn.cursor()

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--proxy-server=http://" + '127.0.0.1:1080')
driver = webdriver.Chrome(options=chrome_options)


def getDownloadUrl(urls):
    kv = {}
    for urla in urls:
        url = urla[0]
        sql = ''
        try:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"准备开始多线程了："+url)
            driver.get(url)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "get完了：" + url)
            download_file_url = driver.execute_script(
                "return window.pl3748.getConfig().playlistItem.allSources[1].file")
            kv[download_file_url] = url
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ":执行到：", url, '没有报错')
        except Exception as e:
            with open('error.log', 'a+') as f:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + str(e), file=f)
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':更新失败，当前更新到：', url,
                      '执行失败的sql是：\n' + str(sql), file=f)
            continue

    insertUrl(kv)


def insertUrl(kv):
    for download_file_url, url in kv.items:
        sql = 'update video_url set download_url ="%s" where url="%s"' % (download_file_url, url)
        print('我是待插入的sql:', sql)
        c.execute(sql)
        conn.commit()
    sql2 = 'SELECT count(*)  from video_url where download_url is null'
    count = c.execute(sql2).fetchall()
    print('插完，还剩下：', count)


def updateDownloadUrl():
    urltable = c.execute('SELECT url  from video_url where download_url is null').fetchall()
    num_proc = 10
    aaaa = {}  # 按照线程数量平均分配到每个线程基本相同的内容
    x = 0
    for i in range(num_proc):
        y = x + len(urltable) // num_proc + 1
        aaaa[i] = urltable[x:y]
        x = y
    thread_list = list()
    for i in range(num_proc):
        t = threading.Thread(target=getDownloadUrl, args=(aaaa[i],))
        thread_list.append(t)

    for t in thread_list:
        t.start()


updateDownloadUrl()
