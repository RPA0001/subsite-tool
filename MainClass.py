import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

def getHTMLText(url):
    print("begin to get "+str(url))
    try:
        session  = HTMLSession()
        res = session.get(url)
        # res.raise_for_status()
        #设置该html文档可能的编码
        res.encoding = res.apparent_encoding
        #返回网页HTML代码
        return res.text
    except:
        return '产生异常'

def getSubsite(i):
    global urls
    global ans
    if urls[i][0][:10] == 'javascript':
        return 
    try:
        demo = getHTMLText(urls[i][0])
        soup = BeautifulSoup(demo, 'html.parser')
        a_labels = soup.find_all('a', attrs={'href': True})
        # 针对缺少https前缀，getHTMLText出错的情况而进行的特判
        if len(a_labels) == 0:
            cnt = 2- ((urls[i][0][0]=='/')+(urls[i][0][1]=='/'))
            demo = getHTMLText('https:'+'/'*cnt+urls[i][0])
            soup = BeautifulSoup(demo, 'html.parser')
            a_labels = soup.find_all('a', attrs={'href': True})
        # 针对herf为相对路径的情况而进行的特判
        if len(a_labels) == 0:
            demo = getHTMLText(urls[urls[i][1]][0]+urls[i][0])
            soup = BeautifulSoup(demo, 'html.parser')
            a_labels = soup.find_all('a', attrs={'href': True})
            if len(a_labels) != 0:
                urls[i][0] = urls[urls[i][1]][0]+urls[i][0]
            else:
                k = 3/0
        else:
            urls[i][0] = 'https:'+'/'*cnt+urls[i][0]
        # 将子网站输出至ans.txt
        ans.writelines('-------------------subsite of :'+str(urls[i][0])+'\n')
        for a in a_labels:
            print(a.get('href'))
            if a not in urls:
                urls.append([a.get('href'),i])
            ans.writelines(str(a.get('href'))+'\n')
        ans.writelines("-------------------"+'\n\n\n')
    except:
        print(str(urls[i][0])+' fail to get subsite')


def main(url):
    #初始化
    global urls
    global limitation
    urls = []
    urls.append([url,0])# urls元素的格式：[网站，父网站序号]
    demo = getHTMLText(url)
    global ans
    ans = open('ans.txt','w')
    file = open('driver.txt','w',encoding='utf-8')# 存放主页的html
    file.write(demo)

    #解析HTML代码
    soup = BeautifulSoup(demo, 'html.parser')

    #模糊搜索HTML代码的所有包含href属性的<a>标签
    a_labels = soup.find_all('a', attrs={'href': True})
    # a_labels = soup.find_all('a', attrs={'data-url': True})
    # li_labels = soup.find_all()
    #获取所有<a>标签中的href对应的值，即超链接
    for a in a_labels:
        print(a.get('href'))
        k = a.get('href')
        if k not in urls:
            urls.append([k,0])

    cnt = 0
    while True:
        if cnt< len(urls) and cnt <= limitation:
            print("cnt = "+str(cnt))
            getSubsite(cnt)
            cnt+=1
        else:
            break
    print("completed")


# 获得网站的最大数量
limitation  = 50
# 第几次获得网站html成功
cnt = 1
# 设置主页
url = 'https://www.zjzwfw.gov.cn/'
main(url)