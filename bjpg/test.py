#coding:utf-8
# import re
# import requests
#
#
# a='http://w123.blog.com/789'
# b=r'(http://w123.blog.com/)(\d+)'
# c=re.match(b,a)
# print c.group(2)
from _ast import Index
import os,statvfs
# vfs=os.stat(r"c:/")
# for i in vfs:
#     print i
#
# print vfs.st_size
# vfs=os.statvfs(r"c:/")
# a=vfs[statvfs.F_BAVAIL]*vfs[statvfs.F_BSIZE]/(1024*1024*1024)
# print a
import os
# def getLinuxDiskInfo(path):
#     if os.path.exists(path):
#         vfs = os.statvfs(path)
#         available=vfs[statvfs.F_BAVAIL]*vfs[statvfs.F_BSIZE]/1024
#         capacity=vfs[statvfs.F_BLOCKS]*vfs[statvfs.F_BSIZE]/1024
#         used = capacity - available
#
#         return available, used, capacity
#
#     return None,None,None
# print r'used\%:%%'%(used/capacity*100)
# print "a%s"%(100)
# used=10.0
# capacity=56


#coding:utf-8
import os,statvfs
def getLinuxDiskInfo(path):
    if os.path.exists(path):
        vfs = os.statvfs(path)
        Avail=round(vfs[statvfs.F_BAVAIL]*vfs[statvfs.F_BSIZE]/1024.0/1024/1024)
        Size=round(vfs[statvfs.F_BLOCKS]*vfs[statvfs.F_BSIZE]/1024.0/1024/1024)
        Used = Size - Avail
        Use=round(Used/Size*100)
        return Size,Used,Avail,Use
a=['Size','Used','Avail','Use%','Mounted on']
b=[]
for x in a:
    b.append(len(x))
d=max(b)
c='/'
b=getLinuxDiskInfo('/')
for x in a:
    print("%-d.4s" % x, end=' ')
print()
for y in b:
    print("%-10.4s" % y + 'G', end=' ')
print("%-10.4s" % c)
#

# a=['size','used','avail','Used','mount on']
# b=['50g','50g','50g','50g','/']
# for x in a:
#     print '{:>5}'.format(x),
#
# print
# for y in b:
#     print '{:>5}'.format(y),
#
# # while  True:
# #     for i in b:
# #         print i+' '*(Index(i))
# #     break
# #思路，获取第一个列表的每一个字段长度，然后+1，
# #然后第二个列表打印的时候，通过前一个列表的长度
# #来输出内容，比如：
# #a1----对应的是b1,b1打印的右边长度为0
# #a2--对应的b2,b2打印的右边长度为a1+1
# #a3--对应的b3，b3打印的右边长度为a1+a2+2
# #a4---对应的b4,b4打印的右边长度为a1+a2+a3+3
# #按照这个思路是有规律可寻的，现在看实现方式
# #第一个是字段长度，直接len就可以获取到了。
# #第二个是打印的位置，
