#-*- coding=utf-8 -*-
# 抓取B站用户信息

"""
UID，用户名，注册时间，生日，地区，投稿视频数，关注数，粉丝数，播放数
"""

from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import pymysql

mysql_host = "localhost"
mysql_port = 3306
mysql_user = "root"
mysql_pwd = "root"
mysql_db = "test"  # 数据库名
mysql_tb = "bilibili_user"  # 表名

conn = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_pwd, port=mysql_port, db=mysql_db,
                       charset="utf8")

# 获取网页数据
def getSoup(start, stop):
    try:
        for number in range(start, stop+1):
            url = 'http://space.bilibili.com/'+str(number)+'/#!/'
            # "http://space.bilibili.com/1643718/#!/"
            # "http://space.bilibili.com/902915/#!/"
            # "http://space.bilibili.com/1/#!/"
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
            )
            # phantomjs.exe的路径G:\Anaconda3\phantomjs\bin
            driver = webdriver.PhantomJS(executable_path='G:\\Anaconda3\\phantomjs\\bin\\phantomjs.exe',
                                         desired_capabilities=dcap)
            driver.get(url)
            time.sleep(1)  # 更据动态网页加载耗时自定义
            content = driver.page_source  # 获取网页内容
            # print(content)
            driver.close()
            soup = BeautifulSoup(content, 'lxml')
            getInfo(soup)
    except Exception:
        pass

# 提取信息
def getInfo(soup):

    try:
        # UID
        uid = int(soup.find_all(attrs={'class': 'item uid'})[0].find_all(attrs={'class': 'text'})[0].contents[0])
        # print(uid)

        # 用户名
        username = soup.find_all(attrs={'id': 'h-name'})[0].contents[0]
        # print(username)

        # 注册时间
        regtime = soup.find_all(attrs={'class': 'item regtime'})[0].find_all(attrs={'class': 'text'})[0].contents[0]
        regdate = time.strftime('%Y-%m-%d', time.strptime(regtime.split(" ")[-1], '%Y-%m-%d'))
        # print(regdate)

        # 生日
        birthdate = soup.find_all(attrs={'class': 'item birthday'})[0].find_all(attrs={'class': 'text'})[0].contents[0]
        birthday = time.strftime('%m-%d', time.strptime(birthdate, '%m-%d'))
        # print(birthday)

        # 地区
        geo = soup.find_all(attrs={'class': 'item geo'})[0].find_all(attrs={'class': 'text'})[0].contents[0]
        # print(geo)

        # 投稿视频数
        videonumber = soup.find_all(attrs={'class': 'count'})[0].contents[0]
        # print(videonumber)
        if '亿' in videonumber:
            truevideonumber = float(videonumber.replace('亿', '')) * 100000000
            # print(truevideonumber)
        elif '万' in videonumber:
            truevideonumber = float(videonumber.replace('万', '')) * 10000
            # print(truevideonumber)
        else:
            truevideonumber = float(videonumber.replace('', ''))
            # print(truevideonumber)

        # 关注数
        gznumber = soup.find_all(attrs={'id': 'n-gz'})[0].contents[0]
        # print(gznumber)
        if '亿' in gznumber:
            truegznumber = float(gznumber.replace('亿', '')) * 100000000
            # print(truegznumber)
        elif '万' in gznumber:
            truegznumber = float(gznumber.replace('万', '')) * 10000
            # print(truegznumber)
        else:
            truegznumber = float(gznumber.replace('', ''))
            # print(truegznumber)

        # 粉丝数
        fansnumber = soup.find_all(attrs={'id': 'n-fs'})[0].contents[0]
        # print(fansnumber)
        # print(gznumber)
        if '亿' in fansnumber:
            truefansnumber = float(fansnumber.replace('亿', '')) * 100000000
            # print(truefansnumber)
        elif '万' in fansnumber:
            truefansnumber = float(fansnumber.replace('万', '')) * 10000
            # print(truefansnumber)
        else:
            truefansnumber = float(fansnumber.replace('', ''))
            # print(truefansnumber)

        # 播放数
        bfnumber = soup.find_all(attrs={'id': 'n-bf'})[0].contents[0]
        # print(bfnumber)
        if '亿' in bfnumber:
            truebfnumber = float(bfnumber.replace('亿', '')) * 100000000
            # print(truebfnumber)
        elif '万' in bfnumber:
            truebfnumber = float(bfnumber.replace('万', '')) * 10000
            # print(truebfnumber)
        else:
            truebfnumber = float(bfnumber.replace('', ''))
            # print(truebfnumber)

        # print('-----------------------------------------')

        saveData(uid, username, regdate, birthday, geo, truevideonumber, truegznumber, truefansnumber, truebfnumber)
    except Exception:
        pass

# 存入数据库
def saveData(uid, username, regdate, birthday, geo, truevideonumber, truegznumber, truefansnumber, truebfnumber):
    try:
        cur = conn.cursor()
        cur.execute("insert into bilibili_user(uid, username, regdate, birthday, geo, videonumber, gznumber, fansnumber, bfnumber)"
                    "values('%d', '%s', '%s', '%s', '%s', '%f', '%f', '%f', '%f')"
                    % (uid, username, regdate, birthday, geo, truevideonumber, truegznumber, truefansnumber, truebfnumber))
        cur.execute("commit;")
        # print('-------已插入数据库--------')
        print(uid)
        cur.close()
    except Exception:
        pass

# 得到最大的uid
def getMaxUid():
    conn = None
    cur = None
    conn = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_pwd, port=mysql_port, db=mysql_db, charset="utf8")
    cur = conn.cursor()

    cur.execute('select max(uid) from bilibili_user;')
    return cur.fetchone()[0]



def main():
    start = getMaxUid()
    if start == None:  # 第一次抓取，指定uid
        start = 1
    print ("user start: ", start)
    stop = int(input("user stop: "))
    getSoup(start, stop)

    # print(soup)




if __name__=='__main__':
    main()


