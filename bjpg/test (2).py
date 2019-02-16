#coding:utf-8
import requests,re
#策略，页面内容返回的是请重新刷新，或者F5，页面内容大小=20，依次作为判断依据，然后进行重试刷新
def one_page_jpg(pagenum):
    basthtml="http://x773721.com/bbs/read.php?tid=1401710"
    html=requests.get(basthtml+pagenum)
    print("当前页面实际返回值是", html.request)
    print("当前页码是", pagenum)
    print("当前页面实际返回值是", html.cookies)
    print("当前页面实际返回值是", html.status_code)
    print("当前页面实际返回值是", html.content())
    print("当前页面实际返回值长度是", len(html.content))
    re_rule=r"http\S*jpg"
    first_re=re.findall(re_rule,html.text)
    second_filter=[]
    for each_url in first_re:
        if each_url not in second_filter:
            second_filter.append(each_url)
    print("图片的个数是", len(second_filter))
    for imgurl in second_filter:
        print("正在下载", imgurl[-17:])


for x in range(0,5):
    y=str(x)
    one_page_jpg(y)
