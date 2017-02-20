# coding:utf-8
import os
import requests,re
HomePage="http://www.mm131.com/"
DownloadPath=r'd:\data\\'
'''
缩写代表的含义：
picture 缩写 img
bug1:下载到这里就卡顿,估计request建立的链接数太多，超过65535了，没有释放，没有达到最大数，卡顿的原因，暂时不说，这里需要优化一
下代码，让打开的页面数减少，下载数减少，访问数减少
requests.exceptions.ConnectionError: HTTPConnectionPool(host='www.mm131.com', port=80):
Max retries exceeded with url: /xinggan/2313_18.html (Caused by NewConnectionError('<requests.packages.urllib3.connection.HTTPConnection object at 0x0000000002A60908>: Failed to establish a new connection: [Errno 10060] ',))
'''
#首页的所有URL地址
HomePageUrl=[]
#所有页面的URL地址
AllUrl=[]
#查找当前URL页面的所有URL
def FindUrl(AnalysisPage):
    WaitAnalysisPage=requests.get(AnalysisPage)
    #正则匹配出所有的，http开头，html结束的URL地址
    RegFindUrl='http\S*\.html'
    RegUrlResult=re.findall(RegFindUrl,WaitAnalysisPage.text)
    #把结果从list中放到set集合里面，去除重复的url地址
    UrlSet=set(RegUrlResult)
    return UrlSet
#查找当前URL页面的所有子页面，也就是2332_1.html类似的页面，没有前缀的
def FindShortUrl(AnalysisPage):
    WaitAnalysisPage=requests.get(AnalysisPage)
    #正则匹配出所有的子页面，也就是以数字开头的1223_，23.html结束的url地址
    RegShortUrl='\d+_\d+\.html'
    RegUrlResult=re.findall(RegShortUrl,WaitAnalysisPage.text)
    ShortUrlSet=set(RegUrlResult)
    return ShortUrlSet
#分析页面的图片地址
def PreDownloadImg(AnalysisPage):
    WaitAnalysisPage=requests.get(AnalysisPage)
    #查找所有的图片URL地址
    RegJpgUrl='http\S*jpg'
    RegUrlResult=re.findall(RegJpgUrl,WaitAnalysisPage.text)
    ShortUrlSet=set(RegUrlResult)
    for EachUrl in ShortUrlSet:
        #查找出来图片的具体URL地址后，执行下载函数
        DownloadImg(EachUrl)
#下载图片的函数
def DownloadImg(ImgUrl):
    #根据http://img1.mm131.com/img/2335/20.jpg，具体的图片地址写入文件
    print "download函数：即将下载的页面是",ImgUrl
    WaitAnalysisPage = requests.get(ImgUrl)
    ImgContent=WaitAnalysisPage.content
    ImgUrlCode=WaitAnalysisPage.status_code
    #超过50KB大小的图片
    if len(ImgContent)>=50000 and ImgUrlCode==200:
        # print "图片访问的返回码是",ImgUrlCode
        #把图片的URL地址转换一下，把斜线转换成横线。从 / 转换成 -，方便在命名的时候直接从url地址取用
        ImgUrlCompile=re.compile(r'/')
        ImgUrlSub=ImgUrlCompile.sub(r'-',ImgUrl)
        #使用with语句直接写入文件
        ImgPath=DownloadPath+ImgUrlSub[7:21]+'\\'
        # print "图片的路径是",ImgPath
        ImgName=ImgUrlSub[22:]
        CreateFolder(ImgPath)
        with open(ImgPath+ImgName, 'wb') as f: f.write(ImgContent)
        print "正在下载",ImgUrl,"页面的图片",ImgName
#创建图片目录
def CreateFolder(FolderPath):
    if not os.path.exists(FolderPath):
        os.makedirs(FolderPath)
#------------------------------------------------
#调用查找当前页面URL的函数
FindUrlResult=FindUrl(HomePage)
#把结果使用extend方法写入到首页url列表中
HomePageUrl.extend(FindUrlResult)
UrlSet=set(HomePageUrl)
print "UrlSet的内容是",UrlSet
print "首页页面URL数量是",len(UrlSet)
#------------------------------------------------
#从首页开始递归查找每一个URL地址
for EachUrlOuter in UrlSet:
    #递归查找每一个页面的子页面
    for EachUrlInner in FindShortUrl(EachUrlOuter):
        #把外层递归的每一个URL地址的纯数字网址后半截，替换为内层递归的值，也就是从2331.html替换为2332_1.html等
        print "外层URL的地址是",EachUrlOuter
        print "内层的URL地址是",EachUrlInner
        RegShortUrl=re.compile(r'\d+.html')
        RegUrlSub=RegShortUrl.sub(EachUrlInner,EachUrlOuter)
        print "替换以后的URL地址是",RegUrlSub
        #替换以后的页面，就是子页面的集合
        EachUrlNew=FindUrl(RegUrlSub)
        AllUrl.extend(EachUrlNew)
        AllUrlSet=set(AllUrl)
        #对于每个子页面，调用下载前分析函数，准备下载
        for EachPage in AllUrlSet:
            print "即将分析的页面是",EachPage
            with open(DownloadPath+'a.txt', 'ab') as f: f.write('\n'+EachPage+'\n')
            PreDownloadImg(EachPage)
        print "已经下载完的图片数量是",len(AllUrlSet)