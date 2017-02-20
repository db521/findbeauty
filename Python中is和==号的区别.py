#coding:utf-8
s=333
b=333.0
#其实python中的is比较的对象很像C语言中的指针,只有地址相同的指针才是同一个指针.
if b is s:#当b指向的内存地址和S一样，条件才成立
    print "right"
print type(b),type(s)#type标识对象的类型
print id(b),id(s)#id用来唯一标识一个对象
if b==s:
    print "good"
#场景二，a,c,d这里的对象都是指向的一个地址
a=1
c=a
d=a
print id(a),id(c),id(d)
if d is c:#当d指向的内存地址和c一样，条件成立
    print "d is c"