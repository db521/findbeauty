#coding:utf-8
import requests,re
def one_page_jpg(pageNum):
    html=requests.get("http://www.jikexueyuan.com/course/pythonbase/?pageNum=2")
    re_rule=r"http\S*jpg"#匹配网页图片
    first_re=re.findall(re_rule,html.text)#查询全面的页面内容，匹配，结果是一个列表
    second_filter=[]#存储正则过滤后的地址
    for each_url in first_re:#把正则匹配出来的图片地址再过滤一遍重复的
        if each_url not in second_filter:
            second_filter.append(each_url)
    path=r'd:\\data\\'#图片存储的路径
    print "图片的个数是",len(second_filter)#打印不重复的图片地址数量
    for imgurl in second_filter:#当前的图片名称个数是从前面的图片列表的长度来定义的
        r=requests.get(imgurl)#打开图片网址
        content=r.content#获取请求的内容
        with open(path+imgurl[-17:], 'wb') as f: f.write(content)#文件的名称使用路径加网址后面的jpg部分作为标题，此处使用了切片操作
        print "正在下载",imgurl[-17:]


