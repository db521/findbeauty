#coding:utf-8
import re


EachUrlOuter='<span class="page-ch">共45页</span>'
a=r'(<span class="page-ch">)(\S+\d)'
c=re.match(a,EachUrlOuter).group(2)
print(c)

