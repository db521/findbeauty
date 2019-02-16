# encoding: utf-8
import json
import os
import re

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


def realUrl(url):
    # url = 'https://voyeurhit.com/videos/daring-teen-at-public-place/'

    r1 = requests.get(url, proxies=proxies, cookies=cookies, verify=False, headers=headers)
    str_url_content = str(r1.content)
    video_path_re = re.search(r'(get_file.*\d)(.*window.jwsettings)', str_url_content)
    video_num_re = re.search(r'(image0.*)(videos_screenshots/)(.*)(/preview.jpg)', str_url_content)
    try:  # get_file/1/f264194d3f6e71df6af6366d73547ae1a3df8f6b4f/||97.64.24.79||1548473170
        urlparm = video_path_re.group(1)
        video_num = video_num_re.group(3)  # 224000/224107
        param = urlparm.split("||")
        get_param = param[0]  # get_file/1/f264194d3f6e71df6af6366d73547ae1a3df8f6b4f/
        realurl = origin + get_param + video_num + '/' + video_num.split('/')[1] + '_hq.mp4/?d=76&br=578&lip=' + \
                  param[1] + '&lt=' + param[2] + '&f=video.m3u8'
        return realurl
    except AttributeError:
        print('找最终下载文件路径失败了，检查一下日志\n')
        with open(url.split('/')[-1:][0]+'-error.log','a+') as f:
            print(url+'\n'+str_url_content,file=f)
        exit(1)



def downloadfile(reurl, url):
    print('reurl:',reurl)
    print('url:',url)
    r1 = requests.get(reurl, proxies=proxies, cookies=cookies, verify=False, headers=headers)
    print('我是有跳转的历史的：',r1.history)
    response_location = r1.history[1].headers['Location']
    preurl = re.search(r'.*mp4', response_location)
    aa = str(r1.content)
    c = aa.split('\\n')
    dirname = url.split('/')[-2:][0]  # 新写一个文件夹
    path = 'g:/mp4/' + dirname
    try:
        os.mkdir(path)
    except:
        print(path + '目录已经存在，不需要创建')
    for x in c:
        if 'seg-' in x:
            finalurl = preurl.group() + '/' + x
            r1 = requests.get(finalurl, proxies=proxies, cookies=cookies, verify=False, headers=headers)
            if r1.status_code == 200:
                file = r1.content
                file_name = x.split('?')[0]
                with open(path + '/' + file_name, 'wb') as file_text:
                    file_text.write(file)
                    print('本次写入文件为：', path + '/' + file_name)
            else:
                print('请求url有问题，不能下载', finalurl, r1.status_code)

    return path


def mergeFile(path):
    os.chdir(path)
    realpath = os.getcwd()
    print('当前所在目录是：', realpath)
    filename = realpath.split('\\')[-1:][0]
    allts = os.listdir(realpath)
    os.chdir(path)
    for x in allts:
        if len(x.split('-')[1]) < 2:  # copy命令没有区分文件名的顺序，是从1、10、11...2、20....开始的，补全一下
            y = '0' + x
            os.system('move ' + x + ' ' + y)

    cmd1 = "copy /b * " + str(filename) + '.mp4'

    cmd2 = "copy  *.mp4 .."
    os.system(cmd1)
    os.system(cmd2)
    os.system('del /Q *.*')


def downall():
    urltable = c.execute('SELECT *  from video_url').fetchall()
    for url in urltable:
        xurl = url[1]
        url1 = realUrl(xurl)
        path = downloadfile(url1, xurl)
        mergeFile(path)
        print('当前执行到：', url[0], xurl)


downall()

#目前存在的问题是：
# ?d=的值是他       aria-valuemax="171.39999999999998">
# &br=578&          这个值不知道去哪里找，明天继续看看
# 文件名下载和存储的路径，还是有点问题，需要再改一下

#https://voyeurhit.com/get_file/1/afbb8ec5fdd41ecb891fdccceb580033b0c1c7de95/5000/5797/5797_hq.mp4/?d=76&br=578&lip=118.26.142.83&lt=1548508237&f=video.m3u8
#https://voyeurhit.com/get_file/1/afbb8ec5fdd41ecb891fdccceb5800331153fbdd8d/5000/5797/5797_hq.mp4/?d=307&br=569&lip=97.64.24.79&lt=1548508136&f=video.m3u8