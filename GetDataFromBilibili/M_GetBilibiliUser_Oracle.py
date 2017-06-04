#-*- coding=utf-8 -*-
# 抓取B站用户信息——多进程并发版本

"""
UID，用户名，注册时间，生日，地区，投稿视频数，关注数，粉丝数，播放数
"""

from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import cx_Oracle as cxo
import SendMessage
from multiprocessing import Pool
import time
import random
import os


oracleHost = '127.0.0.1'
oraclePort = '1521'
oracleUser = 'bilibili'
oraclePassword = '123456'
oracleDatabaseName = 'orcl'
oracleConn = oracleUser + '/' + oraclePassword + '@' + oracleHost + '/' + oracleDatabaseName
conn = cxo.connect(oracleConn)
cursor = conn.cursor()

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
)
dcap["phantomjs.page.settings.resourceTimeout"] = 1000
dcap["phantomjs.page.settings.loadImages"] = False  # 不加载图片，加快速度
dcap["phantomjs.page.settings.disk-cache"] = True  # 启用缓存
dcap["phantomjs.page.settings.userAgent"] = "faking it"
dcap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = False
dcap["phantomjs.page.settings.ignore-ssl-errors"] = True
# phantomjs.exe的路径G:\Anaconda3\phantomjs\bin
driver = webdriver.PhantomJS(executable_path='G:\\Anaconda3\\phantomjs\\bin\\phantomjs.exe',
                             desired_capabilities=dcap)


# 提取信息
def getInfo(soup):

    try:

        # UID
        uid = int(soup.find_all(attrs={'class': 'item uid'})[0].find_all(attrs={'class': 'text'})[0].contents[0])
        # print(uid)

        # 用户名
        username = str(soup.find_all(attrs={'id': 'h-name'})[0].contents[0])
        # print(username)

        # 注册时间
        regtime = soup.find_all(attrs={'class': 'item regtime'})[0].find_all(attrs={'class': 'text'})[0].contents[0]
        regdate = str(time.strftime('%Y-%m-%d', time.strptime(regtime.split(" ")[-1], '%Y-%m-%d')))
        # print(regdate)

        # 生日
        birthdate = soup.find_all(attrs={'class': 'item birthday'})[0].find_all(attrs={'class': 'text'})[0].contents[0]
        birthday = str(time.strftime('%m-%d', time.strptime(birthdate, '%m-%d')))
        # print(birthday)

        # 地区
        geo = str(soup.find_all(attrs={'class': 'item geo'})[0].find_all(attrs={'class': 'text'})[0].contents[0])
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
        cur.execute("insert into bilibili_user(id ,userid, username, regdate, birthday, geo, videonumber, gznumber, fansnumber, bfnumber)"
                    "values(user_seq.Nextval, '%d', '%s', to_date('%s', 'yyyy-MM-dd'), '%s', '%s', '%f', '%f', '%f', '%f')"
                    % (uid, username, regdate, birthday, geo, truevideonumber, truegznumber, truefansnumber, truebfnumber))
        cur.execute("commit")
            # print('-------已插入数据库--------')
        print(uid)
        cur.close()

        # if uid%100 == 0:
        #     msg = '已抓取并导入'+str(uid)+'条用户信息'
        #     SendMessage.sendMessage('东京中央软体产业株式会社', msg)
        #     print(msg)

    except Exception:
        pass

# 得到最大的uid
def getMaxUid():
    cursor.execute('select max(userid) from bilibili_user')
    return cursor.fetchone()[0]



def main(number):
    url = 'http://space.bilibili.com/' + str(number) + '/#!/'
    try:
        driver.get(url)
        # time.sleep(random.uniform(1, 5))  # 更据动态网页加载耗时，此处为随机时间
        content = driver.page_source  # 获取网页内容
        # print(content)
        # driver.close()
        # driver.close()
        # driver.quit()  # 仅仅close不能解决问题，要使用quit，避免因phantomjs造成内存泄露
        soup = BeautifulSoup(content, 'lxml')
        getInfo(soup)
        # print(int(soup.find_all(attrs={'class': 'item uid'})[0].find_all(attrs={'class': 'text'})[0].contents[0]))
    except Exception:
        pass



if __name__=='__main__':
    time1 = time.time()

    start = getMaxUid()  # 抓取范围
    stop = start + 100
    print(start, stop)

    try:
        pool = Pool(processes=10)  # 设定并发进程的数量
        pool.map(main, (i for i in range(start+1, stop+1)))
    except Exception:
        pass

    command = 'taskkill /f /t /im phantomjs.exe'
    os.system(command)  # 杀掉phantomjs进程

    time2 = time.time()
    print((time2 - time1) / 60, u"分钟")








