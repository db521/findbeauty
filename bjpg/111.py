#coding:utf-8
import re
s="http://10.211.93.207:9098/aserver/portalengine/getIdentityIDByAccount"
# match_result= re.search(r'[\d.]+:[\d]+',s)
# print match_result
# print match_result.group()
p=re.compile(r'([\d.]+:[\d]+)')
print(p.sub(r'192.168.3.111:1111', s))
#raw_input是为了让Python的脚本直接运行时候，不会一闪而过，而是页面等待用户输入回车后，才会消失
#raw_input()
logfile=open(r'd:\\hello.txt','w+')
#print 既可以把内容输出到屏幕，也可以使用>>输出到日志文件
with logfile as f:
    print("error,我要把print的内容写入日志中",file=f)
logfile.close()

a=" noinspection PyTypeChecker"
#和range函数类型，但是range函数只能循环索引或者元素
for s in enumerate(a):
    print(s)
for s in range(a):#这个命令执行失败
    print(s)
for s in range(len(a)):#range还只能使用int类型，不能使用str类型
    print(s)
