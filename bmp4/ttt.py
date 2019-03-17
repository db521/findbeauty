#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/3/14 21:13 
# @File : ttt.py 
# coding=utf-8
import os
import re
import threading
import time

import requests
import sqlite3
# systemctl start docker
# docker run --name dnginx -p 999:80   -v /root/bmp4/mp4:/usr/share/nginx/html:ro -d nginx
# -v /root/bmp4/nginx/default.conf:/etc/nginx/conf.d/default.conf
# docker cp dnginx:/etc/nginx/conf.d/default.conf .
# docker logs -f dnginx
# 97.64.24.79
# 118.26.142.94
#  allow 118.26.142.94;
#   allow 97.64.24.79;
#   deny all;
#  autoindex on;
#  autoindex_exact_size off;
# autoindex_localtime on
# docker rm -f dnginx

# conn = sqlite3.connect('test.db')
# c = conn.cursor()
# alld = c.execute('select durtime from bigvides').fetchall()
# i=1
# for x in alld:
#     minite = int(x[0].split(':')[0])
#
#     if minite < 10:
#         i+=1
#         # print('当前minite:',minite)
#         c.execute('delete from bigvides where durtime=%s' % ('"'+x[0]+'"'))
#         print('我删除了:', x)
# conn.commit()
# c.close()
# print('一共删除了:',i)
# docker run -d -p 80:80 -e NOSSL=1 -v /opt/moinmoin-data:/usr/local/share/moin/data --name mwiki olavgg/moinmoin-wiki
# docker run -d --name ftp -p 21:21 -p 30000-30009:30000-30009 -v /root/bmp4/mp4:/root/bmp4/mp4 -e FTP_USER_NAME=db520 -e FTP_USER_PASS=131415aA~ -e FTP_USER_HOME=/root/bmp4/mp4  stilliard/pure-ftpd:hardened
# docker run --name mwiki -p 80:80 -d mediawiki
# docker run -d \
 -p 80:80  --name dokuwiki  \
 bitnami/dokuwiki:latest
# cZ3c9DKOGFXY
# 28690
