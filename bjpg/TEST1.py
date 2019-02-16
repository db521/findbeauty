# coding:utf-8
import os
import requests,re
HomePage="http://www.mm131.com/"
DownloadPath=r'd:\data\\'
#首页的所有URL地址
HomePageUrl=[]
#所有页面的URL地址
AllUrl=[]
def FindUrl(AnalysisPage):
    """#查找当前URL页面的所有URL"""
    WaitAnalysisPage=requests.get(AnalysisPage)
    RegFindUrl='http\S*\.html'
    RegUrlResult=re.findall(RegFindUrl,WaitAnalysisPage.text)
    UrlSet=set(RegUrlResult)
    return UrlSet
def PreDownloadImg(AnalysisPage):
    """分析页面内容"""
    WaitAnalysisPage=requests.get(AnalysisPage)
    RegJpgUrl='http\S*1.jpg'#查找所有的图片地址
    ImgSumRe=re.compile(r'(共)(\d+)')#查找当前页面的图片个数
    ImgNumRe=r'/1.jpg'#替换url地址后面的数字部分
    ImgNameRe=re.compile(r'(<h5>)(\S+)(</h5>)')#查找当前标题
    RegSumResult=re.search(ImgSumRe,WaitAnalysisPage.text).group(2)
    RegUrlResult=re.findall(RegJpgUrl,WaitAnalysisPage.text)
    NumResult=range(1,len(RegSumResult))
    ImgNameResult=re.search(ImgNameRe,WaitAnalysisPage.text).group(2)
    UrlSet=set(RegUrlResult)
    for EachUrl in UrlSet:
        print("当前页面是", EachUrl)
        print("当前主题的图片个数是", len(RegSumResult))
        print("当前页面的标题是", ImgNameResult)
        for num in NumResult:
            RegUrlSec=ImgNumRe.sub('/'+str(num)+'.jpg',EachUrl)
            print("当前页面相关的URL是", RegUrlSec)
            # DownloadImg(RegUrlSec,ImgNameResult)

def DownloadImg(ImgUrl,ImgName):
    """下载图片的函数,根据http://img1.mm131.com/img/2335/20.jpg，具体的图片地址写入文件,只处理超过50KB大小的图片"""
    WaitAnalysisPage = requests.get(ImgUrl)
    ImgContent=WaitAnalysisPage.content
    if len(ImgContent)>=50000:
        #把图片的URL地址转换一下，把斜线转换成横线。从 / 转换成 -，方便在命名的时候直接从url地址取用
        ImgUrlCompile=re.compile(r'/')
        ImgUrlSub=ImgUrlCompile.sub(r'-',ImgUrl)
        #使用with语句直接写入文件
        ImgPath=DownloadPath+ImgUrlSub[7:21]+'\\'
        ImgName=ImgUrlSub[22:]

        CreateFolder(ImgPath)
        with open(ImgPath+ImgName, 'wb') as f: f.write(ImgContent)
        print("正在下载", ImgUrl, "页面的图片", ImgName)


def CreateFolder(FolderPath):
    """创建图片目录"""
    if not os.path.exists(FolderPath):
        os.makedirs(FolderPath)
#------------------------------------------------
#调用查找当前页面URL的函数
FindUrlResult=FindUrl(HomePage)
#把结果使用extend方法写入到首页url列表中
HomePageUrl.extend(FindUrlResult)
UrlSet=set(HomePageUrl)
print("UrlSet的内容是", UrlSet)
print("首页页面URL数量是", len(UrlSet))
#------------------------------------------------
#从首页开始递归查找每一个URL地址
for EachUrlOuter in UrlSet:
    PreDownloadImg(EachUrlOuter)

