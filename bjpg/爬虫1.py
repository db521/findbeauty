# -*- coding: utf-8 -*-
import urllib,re,time,os

def schedule(a,b,c):#显示下载进度
  per = 100.0*a*b/c#  a:已经下载的数据块
  if per > 100 :#b:数据块的大小
    per = 100#  c:远程文件的大小
  print('%.2f%%' % per)


def getHtml(url):
  page = urllib.urlopen(url)
  html = page.read()
  return html
  #print html
def downloadImg(html):
  #reg = r'src="(.+?\.jpg)"' #xiao77用
  reg = r'src="(.+?\.jpg)"'
  imgre = re.compile(reg)
  #print imgre
  imglist = re.findall(imgre, html)#图片列表
  #print imglist
  t = time.localtime(time.time())  #定义文件夹的名字
  foldername = str(t.__getattribute__("tm_year"))+"-"+str(t.__getattribute__("tm_mon"))+"-"+str(t.__getattribute__("tm_mday"))
  picpath = 'D:\\ImageDownload\\%s' % foldername  #下载到的本地目录
  if not os.path.exists(picpath):   #路径不存在时创建一个
    os.makedirs(picpath)
  x = 0
  for imgurl in imglist:
        target = picpath+'\\%s.jpg' % x
        print('Downloading image to location: ' + target + '\nurl=' + imgurl)
        image = urllib.urlretrieve(imgurl, target, schedule)
        x += 1
        return image
if __name__ == '__main__':
  html = getHtml("http://www.baidu.com")
  downloadImg(html)
  print("Download has finished.")
