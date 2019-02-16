#coding:utf-8
from random import random
import re
s="http://10.211.93.207:9098/aserver/portalengine/getIdentityIDByAccount"
p=re.compile(r'([\d.]+:[\d]+)')
for a in range(1,11):
    x=random()
    b0=str(x)
    x1=x+100
    b1=str(x1)
    print (p.sub(b0+"/"+b1,s))