#coding:utf-8

#https://zhuanlan.zhihu.com/p/20810469?refer=auxten参考地址
import requests
import threading

class downloader:
    # 构造函数
    def __init__(self):
        # 设置url
        self.url='http://51reboot.com/src/blogimg/pc.jpg'
        # 设置线程数
        self.num=8
        # 文件名从url最后取
        self.name=self.url.split('/')[-1]
        # 用head方式去访问资源
        r = requests.head(self.url)
        # 取出资源的字节数
        self.total = int(r.headers['Content-Length'])
        print('total is %s' % (self.total))

    def get_range(self):
        ranges=[]
        # 比如total是50,线程数是4个。offset就是12
        offset = int(self.total/self.num)
        for i in  range(self.num):
            if i==self.num-1:
                # 最后一个线程，不指定结束位置，取到最后
                ranges.append((i*offset,''))
            else:
                # 没个线程取得区间
                ranges.append((i*offset,(i+1)*offset))
        # range大概是[(0,12),(12,24),(25,36),(36,'')]
        return ranges

    def download(self,start,end):
        headers={'Range':'Bytes=%s-%s' % (start,end),'Accept-Encoding':'*'}
        # 获取数据段
        res = requests.get(self.url,headers=headers)
        # seek到指定位置
        print('%s:%s download success' % (start, end))
        self.fd.seek(start)
        self.fd.write(res.content)
    def run(self):
        # 打开文件，文件对象存在self里
        self.fd =  open(self.name,'w')
        thread_list = []

        n = 0
        for ran in self.get_range():
            start,end = ran
            print('thread %d start:%s,end:%s' % (n, start, end))
            n+=1
            # 开线程
            thread = threading.Thread(target=self.download,args=(start,end))
            thread.start()
            thread_list.append(thread)
        for i in thread_list:
            # 设置等待
            i.join()
        print('download %s load success' % (self.name))
        self.fd.close()
if __name__=='__main__':
    # 新建实例
    down = downloader()
    # 执行run方法
    down.run()