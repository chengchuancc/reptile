#https://blog.csdn.net/qq_45720042/article/details/115312318
import os
import bs4
import re
import time
import requests
from bs4 import BeautifulSoup

def getHTMLText(url, headers):
    """向目标服务器发起请求并返回响应"""
    try:
        r = requests.get(url=url, headers=headers)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "html.parser")
        return soup
    except:
        return ""

def CreateFolder():
    """创建存储数据文件夹"""
    flag = True
    while flag == 1:
        file = input("请输入保存数据文件夹的名称：")
        if not os.path.exists(file):
            os.mkdir(file)
            flag = False
        else:
            print('该文件已存在，请重新输入')
            flag = True
            
    # os.path.abspath(file)  获取文件夹的绝对路径
    path = os.path.abspath(file) + "\\"
    return path

def GetType():
    print("1:日历\n 2:动漫\n 3:风景\n 4:美女\n 5:游戏\n")
    print("6:影视\n 7:动态\n 8:唯美\n 9:设计\n 10:可爱\n")
    print("11:汽车\n 12:花卉\n 13:动物\n 14:节日\n 15:人物\n")
    print("16:美食\n 17:水果\n 18:建筑\n 19:体育\n 20:军事\n")
    print("21:非主流\n 22:其他\n 23:王者荣耀\n 24:护眼\n 25:LOL\n")
    type = input("请输入需要获取的图片类型")
    if type == "1":
        t = "/rili"
    elif type == "2":
        t = "/dongman"
    elif type == "3":
        t = "/fengjin"
    elif type == "4":
        t = "/meinv"
    elif type == "5":
        t = "/youxi"
    elif type == "6":
        t = "/yinshi"
    elif type == "7":
        t = "/dongtai"
    elif type == "8":
        t = "/weimei"
    elif type == "9":
        t = "/sheji"
    elif type == "10":
        t = "/keai"
    elif type == "11":
        t = "/qiche"
    elif type == "12":
        t = "/huahui"
    elif type == "13":
        t = "/dongwu"
    elif type == "14":
        t = "/jieri"
    elif type == "15":
        t = "/renwu"
    elif type == "16":
        t = "/meishi"
    elif type == "17":
        t = "/shuiguo"
    elif type == "18":
        t = "/jianzhu"
    elif type == "19":
        t = "/tiyu"
    elif type == "20":
        t = "/junshi"
    elif type == "21":
        t = "/feizhuliu"
    elif type == "22":
        t = "/qita"
    elif type == "23":
        t = "/wangzherongyao"
    elif type == "24":
        t = "/huyan"
    elif type == "25":
        t = "/s/lol"
    print (t)
    return t

def fillUnivList(ulist, soup):
    """获取每一张图片的原图页面"""
    # [0]使得获得的ul是 <class 'bs4.BeautifulSoup'> 类型
    div = soup.find_all('div', 'list')[0]
    for a in div('a'):
        if isinstance(a, bs4.element.Tag):
            hr = a.attrs['href']
            href = re.findall(r'/desk/[1-9]\d{4}.htm', hr)
            if bool(href) == True:
                ulist.append(href[0])

    return ulist


def DownloadPicture(left_url,list,path):
    for right in list:
        url = left_url + right
        r = requests.get(url=url, timeout=10)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text,"html.parser")
        tag = soup.find_all("p")
        # 获取img标签的alt属性，给保存图片命名
        name = tag[0].a.img.attrs['alt']
        img_name = name + ".jpg"
        # 获取图片的信息
        img_src = tag[0].a.img.attrs['src']
        try:
            img_data = requests.get(url=img_src)
        except:
            continue

        img_path = path + img_name
        with open(img_path,'wb') as fp:
            fp.write(img_data.content)
        print(img_name, "   ******下载完成！")

def PageNumurl(urls,type):
    num = int(input("请输入爬取所到的页码数："))
    for i in range(2,num+1):
        u = "http://www.netbian.com"+str(type)+"/index_" + str(i) + ".htm"
        urls.append(u)

    return urls


if __name__ == "__main__":
    uinfo = []
    # 选择需要爬取的图片类型
    type = GetType()
    left_url = "http://www.netbian.com"
    urls = ["http://www.netbian.com"+str(type)+"/index.htm"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    }
    start = time.time()
    # 1.创建保存数据的文件夹
    path = CreateFolder()
    # 2. 确定要爬取的页面数并返回每一页的链接
    PageNumurl(urls,type)
    n = int(input("访问的起始页面："))
    for i in urls[n-1:]:
        # 3.获取每一个页面的首页数据文本
        soup = getHTMLText(i, headers)
        # 4.访问原图所在页链接并返回图片的链接
        page_list = fillUnivList(uinfo, soup)
        # 5.下载原图
        DownloadPicture(left_url, page_list, path)

    print("全部下载完成！", "共" + str(len(os.listdir(path))) + "张图片")
    end = time.time()
    print("共耗时" + str(end-start) + "秒")
