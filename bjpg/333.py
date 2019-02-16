#!/usr/bin/python
# -*- coding:utf-8 -*-

import os, errno
import datetime, time
def bakup(ip1):
    if ip1==192:
        print ip1
    return bakup
def ip1(args):
    print "ip1被调用了"


@bakup(bakup)
def ip(ip1):
    ip1=[192]
    print "调用了"
