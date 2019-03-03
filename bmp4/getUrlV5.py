#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/3/2 10:36 
# @File : getUrlV5.py
import os
import re
import threading
import time
from random import randint

import urllib3
from requests.exceptions import ProxyError
from selenium.common.exceptions import WebDriverException, TimeoutException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from bs4 import BeautifulSoup

import sqlite3
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

with open('temp.txt', 'r') as f:
    soup = BeautifulSoup(f, "html.parser")


class Download:
    def __init__(self):
        self.conn = sqlite3.connect('test.db', check_same_thread=False)
        self.c = self.conn.cursor()
        self.cookies = {
            'cookies': '__cfduid=d1a50478a43f118736847d328be2cceab1548462867; __auc=18766a7b1688794bd51aa5ed3ed; '
                       '_ga=GA1.2.1831337609.1548462899; _ym_uid=1548462899440317366; _ym_d=1548462899; '
                       'PHPSESSID=6q1fsaso7vg7j8hh62nbm5ikb1; kt_ips=97; kt_tcookie=1; kt_is_visited=1; '
                       '_gid=GA1.2.1637991732.1551486589; _ym_isad=1; visitCount=19; splashWeb-645543-42=1; '
                       'nb-no-req-645543=true; '
                       'video_log=two-chinese-babe-toilet-voyeur%3A1551535385%3Bdaring-teen-at-public-place'
                       '%3A1551611745%3Bhidden-cam-under-desk-caught-my-mom-masturbating%3A1551611865%3B; tcout_c=1; '
                       'kt_qparams=dir%3Ddaring-teen-at-public-place; countcli=1551700723670; '
                       '__asc=a5e79c0d16943b8223bb7f5e0f9; _ym_visorc_23521642=b; '
                       '__atuvc=0%7C6%2C0%7C7%2C0%7C8%2C12%7C9%2C7%7C10; __atuvs=5c7bd50524dc2aa5001'}
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/69.0.3497.81 Safari/537.36'}
        self.proxies = {'https': 'https://127.0.0.1:1080'}
        self.caturl = 'https://voyeurhit.com/categories/'
        self.mp4url = 'https://voyeurhit.com/videos/'
        self.path = 'g:/mp4/'
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.chrome_options.add_experimental_option("prefs", prefs)
        self.chrome_options.add_argument("--proxy-server=http://" + '127.0.0.1:1080')

    def homepage(self):  # 首页解析目录和当前页的视频
        catdict = {}
        mp4dict = {}
        for link in soup.find_all('a'):
            try:
                url = link.get('href')
                if self.caturl in url:  # 获取目录url
                    nums = re.sub('\D', '', link.contents[-1])  # tag的 .contents 属性可以将tag的子节点以列表的方式输出
                    remain = int(nums) % 60
                    times = int(nums) // 60 + 1 if remain else int(nums) // 60
                    catname = url.replace(self.caturl, '').rstrip('/')
                    catdict[catname] = times
            except TypeError:
                print('homepage报错了：' + repr(link))
                continue
        self.inserttable(catdict, table_name='categories')
        self.inserttable(mp4dict, table_name='videos')

    def getvideoinfo(self, link):  # 获取单个video的基础信息：时长、人数、评分、视频id
        # link指的是视频的a标签
        child = link.contents
        durtime = child[1].text
        video_id = child[1].contents[0]['data-video-id']
        info = child[5].text  # info的div
        review = re.search('(Views: )(\d+)', info)
        views = review.group(2) if review else 0
        rerat = re.search('(\d+)(%)', info)
        rat = rerat.group(1) if rerat else 0

        return durtime, video_id, views, rat

    def inserttable(self, tabledict, table_name):  # 只负责插入表
        sql = ''
        try:
            for k, v in tabledict.items():
                if table_name == 'videos':
                    sql = "insert into videos(access_url,durtime, video_id, views, rat,category)VALUES (%s,%s,%d,%d,%d,%s)" % (
                        '"' + k + '"', '"' + v[0] + '"', int(v[1]), int(v[2]), int(v[3]), '"' + v[4] + '"')
                elif table_name == 'dload':
                    sql = "insert into dload(download_url,video_id)VALUES (%s,%d)" % ('"' + k + '"', v)
                elif table_name == 'categories':
                    sql = f"insert into categories(cat_url,times)VALUES (%s,%d)" % ('"' + k + '"', v)
                elif table_name == 'dlog':
                    sql = "insert into dlog(url,max)VALUES (%s,%d)" % ('"' + k + '"', v)

                lock = threading.Lock()
                try:
                    lock.acquire(True)
                    self.c.execute(sql)
                    with open('insert.log', 'a+') as f:
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '我是即将入库的sql:', sql, file=f)
                except sqlite3.IntegrityError:
                    continue
                except sqlite3.ProgrammingError:
                    with open('errorsql.log', 'a+') as f1:
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '我是入库失败的sql:', sql, file=f1)
                    lock.acquire(True)
                    self.c.execute(sql)
                finally:
                    lock.release()
        finally:
            self.conn.commit()
            print('/' * 40)
            print('提交了一波：', len(tabledict))
            print('/' * 40)

    def getdurl(self, url_id):  # 只负责获取插入dload表的数据
        url_id_dict = {}
        i = 0
        driver = webdriver.Chrome(options=self.chrome_options)
        try:
            for k, v in url_id:
                gurl = self.mp4url + k + '/'
                try:
                    driver.get(gurl)
                    aurl = gurl.replace(self.mp4url, '').rstrip('/')
                    with open('sucess.log', 'a+') as f:
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "get完了：" + aurl, v, file=f)
                    download_url = driver.execute_script(
                        "return window.pl3748.getConfig().playlistItem.allSources[1].file")
                    with open('sucess.log', 'a+') as f:
                        print('获取到值了：' + download_url, file=f)
                    url_id_dict[download_url] = v
                except TimeoutException:
                    driver.quit()
                except WebDriverException:
                    print('/' * 40)
                    print('没有获取到值，退出浏览器，重新来')
                    print('/' * 40)
                driver.quit()
            print('/' * 40)
            print('待入库的数量为：', len(url_id_dict))
            self.inserttable(url_id_dict, table_name='dload')
            print('/' * 40)
        except Exception as e:
            print(e)
        finally:
            driver.quit()
            i += 1
            print(threading.currentThread(), ' :线程已经处理了：', i, '/', len(url_id))
            self.inserttable(url_id_dict, table_name='dload')

    def getvideo(self, names_times):  # 插入videos表
        mp4dict = {}  # 存视频及基础信息
        dlogdict = {}  # 存已经下载过的视频
        for cat_name, times in names_times:
            for i in range(1, times + 1):
                rurl = self.caturl + cat_name + '/' + str(i) + '/'
                print(threading.currentThread(), '当前目录url：' + rurl)
                try:
                    r = requests.get(rurl, proxies=self.proxies, cookies=self.cookies, verify=False,
                                     headers=self.headers)
                    if r.status_code == 200:
                        soup1 = BeautifulSoup(r.text, "html.parser")

                        for link in soup1.find_all('a'):
                            try:
                                url2 = link.get('href')
                                if self.mp4url in url2:
                                    durtime, video_id, views, rat = self.getvideoinfo(link)  # 获取视频基础信息
                                    access_url = url2.replace(self.mp4url, '').rstrip('/')
                                    mp4dict[access_url] = [durtime, video_id, views, rat, cat_name]
                            except TypeError:
                                continue
                    else:
                        print('此处异常', rurl)
                except ProxyError:
                    print('代理连接数太多了，等5秒钟，释放一下再开新的线程')
                    time.sleep(5)
            dlogdict[cat_name] = times

            print(threading.currentThread().ident, '一次大循环完事了:' + cat_name)
            self.inserttable(mp4dict, table_name='videos')  # 入库
            self.inserttable(dlogdict, table_name='dlog')  # 入库
            mp4dict = {}
            continue

    def dfile(self, url_file):  # 根据文件名和下载地址直接写入文件夹
        for filename, durl in url_file:
            file_name = filename + '.mp4'
            absfile = self.path + file_name
            if not os.path.exists(absfile):
                r1 = requests.get(durl, proxies=self.proxies, cookies=self.cookies, verify=False,
                                  headers=self.headers)
                if r1.status_code == 200:
                    file1 = r1.content
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':开始写入文件：：', absfile)
                    with open(absfile, 'wb') as file_text:
                        file_text.write(file1)
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':写入成功!文件为：：', absfile)
                else:
                    with open('error.log', 'a+') as f1:
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '请求url有问题，不能下载', durl, file_name,
                              r1.status_code, file=f1)
            else:
                print(file_name + '文件已经存在了，继续下载下一个')

    def newT(self, sql, type):  # 启动线程的数量,type=1是插入dload库，=0是执行下载函数
        alljob = self.c.execute(sql).fetchall()
        print('总任务数是：', len(alljob))
        num_proc = 3
        # 如果任务数/线程数<=2，就直接拆分为1份就可以
        singlejob = len(alljob) // num_proc + 1 if len(alljob) // num_proc + 1 > 2 else len(alljob) // num_proc
        equal_mount_job = [alljob[x:x + singlejob] for x in range(0, len(alljob), singlejob)]  # 按照线程数量平均分配到每个线程基本相同的活
        thread_list = list()
        for i in range(num_proc):
            if type == 1:
                target = self.getdurl
            elif type == 0:
                target = self.dfile
            else:
                target = self.getvideo
            print(threading.currentThread(), '线程任务数：', len(equal_mount_job[i]))
            t = threading.Thread(target=target, args=(equal_mount_job[i],))  # 平均分配后的一个列表传给下载函数
            thread_list.append(t)

        for t in thread_list:
            t.start()


if __name__ == '__main__':
    jobdload = 'select v.access_url,d.download_url from videos v,dload d where v.video_id=d.video_id'
    # Download().newT(jobdload,type=0)#多线程下载
    jobdurlinsert = 'select access_url,video_id from videos where video_id not in (select video_id from dload)'
    # Download().newT(jobdurlinsert, type=1)  # getdurl 多线程入库

    jobvideo = 'SELECT cat_url,times  from categories where cat_url not in (select url from dlog)'  # 总的数量
    # Download().newT(jobvideo, type=2)  # 多线程入库
    conn = sqlite3.connect('test.db', check_same_thread=False)
    c = conn.cursor()
    Download().getdurl(c.execute(jobdurlinsert).fetchall())