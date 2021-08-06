
import re
import requests
from bs4 import BeautifulSoup
import os
import time
import sys
from tqdm import tqdm


path = 'pic/'

def crawl_wiki_data(tpye,list_str,start_page,stop_page):
    """爬取html"""
    headers = { 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62"
    }
    pic_urls = []
    start_page = int(start_page)
    stop_page = int(stop_page)
    for page in range(start_page,stop_page+1):
        # url=url+str(page)
        # print(url)
        if (page == 1):
            url='https://www.mm131.net/' + tpye
        else:
            url='https://www.mm131.net/' + tpye + list_str + str(page) + '.html'
        print("-------------------------lsp----------------------------------")
        print("这是第%s页" %(page))
        print(url)
        response = requests.get(url,headers=headers)
        #print(response.status_code)
        soup=BeautifulSoup(response.content,'lxml')
        #print(soup)
        content=soup.find('body')
        # parse_wiki_data(content)
        pattern = "(?<=https://www.mm131.net/"+tpye+").*?(?=.html)"
        str_html = str(soup)
        gruop_num = re.findall(pattern, str_html)
        pattern = '(?<=width="120"/>).*?(?=</a>)'
        str_html = str(content)
        gruop_name = re.findall(pattern, str_html)
        length = len(gruop_name)
        for i in range(0,length):
            stime=time.time()
            group_url = 'https://www.mm131.net/' + tpye + str(gruop_num[i]) + ".html"
            response = requests.get(group_url,headers=headers)
            #print(response.status_code)
            soup=BeautifulSoup(response.content,'lxml')
            content=soup.find('body')
            pattern = "(?<=共).*?(?=页)"
            str_html = str(content)
            str_page = re.findall(pattern, str_html)
            num_page = int(str_page[0])#图片的数量
            
            for j in range(1,num_page+1):
                pic_url = "https://img1.hnllsy.com/pic/" + str(gruop_num[i]) + "/" + str(j) + ".jpg"
                pic_urls.append(pic_url)
            down_pic(gruop_name[i],pic_urls,num_page)#下载图片

            pic_urls = []
            etime=time.time()
            print('耗时%s秒' %(etime-stime))
        

def down_pic(name,pic_urls,num_page):
    """下载图片"""
    print("%s -- 共有%s张图片" %(name,num_page))
    gruop_dir = path + name + '/'
    headers={"Referer": "https://www.mm131.net/",
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62"}
    if not os.path.exists(gruop_dir):
        os.makedirs(gruop_dir)
    with tqdm(total=num_page,desc = 'LSP下载进度' ) as phbr:
        for i,pic_url in enumerate(pic_urls):
            try:
                time1=time.time()
                pic = requests.get(pic_url,headers=headers)  
                string = name+str(i+1)+'.jpg'
                with open(gruop_dir+string,'wb') as f:
                    #print('LSP成功下载第%s张图片:%s' %(str(i+1),str(pic_url)),name)
                    f.write(pic.content)
                    #print('\r %s:LSP成功下载第%s张图片' %(str(name),str(i+1)),end="")
                    time3=time.time()-time1
                    phbr.update(1)

            except Exception as e:
                    print('下载第%s张图片时失败:%s' %(str(i+1),str(pic_url)))
                    print(e)
                    continue
            
def GetType():
    print("1:性感\n 2:清纯\n 3:校花\n 4:车模\n 5:旗袍\n 6:明星\n")

    type = input("请输入需要获取的图片类型：")
    if type == "1":
        t = "xinggan/"
        t1 = "list_6_"
        
    elif type == "2":
        t = "qingchun/"
        t1 = "list_1_"
    elif type == "3":
        t = "xiaohua/"
        t1 = "list_2_"
    elif type == "4":
        t = "chemo/"
        t1 = "list_3_"
    elif type == "5":
        t = "qipao/"
        t1 = "list_4_"
    elif type == "6":
        t = "mingxing/"
        t1 = "list_5_"

    return t,t1

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

if __name__ == '__main__':

    tpye,list_str=GetType()    
    path = CreateFolder()
    print('已经为LSP创建好了目录：%s' %(path))
    start_page = input("从第几页开始抓取：")
    stop_page = input("抓取到第几页：")
    crawl_wiki_data(tpye,list_str,start_page,stop_page)


    print("所有信息爬取完成！谢谢")
