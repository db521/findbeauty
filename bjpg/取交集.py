#coding:utf-8
# a=1
# b=2
# print "%s你说啥%s"%(a,b)
#取交集方法
l=[]
a=[1,2,3]
b=[2,3,5]
for m in a:
    if m in b:
        l.append(m)
print(l)
