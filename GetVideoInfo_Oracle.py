#-*- coding=utf-8 -*-
# 抓取B站视频信息

"""
av号，up主userid，视频标题，发布时间，点击数，弹幕数，硬币数，收藏数，大分类，小分类，分享数，标签，视频描述
"""

import urllib
import urllib.request
from bs4 import BeautifulSoup
from io import BytesIO
import gzip
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import re
import cx_Oracle as cxo
from wxpy import *


oracleHost = '127.0.0.1'
oraclePort = '1521'
oracleUser = 'bilibili'
oraclePassword = '123456'
oracleDatabaseName = 'orcl'
oracleConn = oracleUser + '/' + oraclePassword + '@' + oracleHost + '/' + oracleDatabaseName
conn = cxo.connect(oracleConn)
cursor = conn.cursor()

# 获取网页数据
def getSoup(start, stop):
    try:
        for number in range(start, stop + 1):
            url = 'http://www.bilibili.com/video/av'+str(number)+'/'
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
            )
            dcap["phantomjs.page.settings.loadImages"] = False
            # phantomjs.exe的路径G:\Anaconda3\phantomjs\bin
            driver = webdriver.PhantomJS(executable_path='G:\\Anaconda3\\phantomjs\\bin\\phantomjs.exe',
                                         desired_capabilities=dcap)
            driver.get(url)
            # time.sleep(1)  # 更据动态网页加载耗时自定义
            content = driver.page_source  # 获取网页内容
            driver.close()
            soup = BeautifulSoup(content, 'lxml')
            getInfo(soup)
    except Exception:
        pass



def getInfo(soup):
    try:
        # av号
        avid = int(re.findall(r'.*aid=(.*)">.*', str(soup.find_all('span', attrs={'class': 't fav_btn'})[0]))[0])
        # print(avid)

        # up主userid
        userid = int(re.findall(r'.*mid="(.*)">.*', str(soup.find_all('div', attrs={'class': 'upinfo'})[0]))[-1])
        # print(userid)

        # 视频标题
        title = str(soup.find_all('div', attrs={'class': 'v-title'})[0].contents[0].contents[0])
        # print(title)

        # 发布时间
        uptime = str(soup.find_all('time', attrs={'itemprop': 'startDate'})[0].contents[0].contents[0])
        # print(uptime)

        # 点击数
        djnumber = str(soup.find_all('span', attrs={'id': 'dianji'})[0].contents[0])
        # print(djnumber)
        if '亿' in djnumber:
            truedjnumber = float(djnumber.replace('亿', '')) * 100000000
            # print(truedjnumber)
        elif '万' in djnumber:
            truedjnumber = float(djnumber.replace('万', '')) * 10000
            # print(truedjnumber)
        else:
            truedjnumber = float(djnumber.replace('', ''))
            # print(truedjnumber)

        # 弹幕数
        dmnumber = str(soup.find_all('span', attrs={'id': 'dm_count'})[0].contents[0])
        # print(dmnumber)
        if '亿' in dmnumber:
            truedmnumber = float(dmnumber.replace('亿', '')) * 100000000
            # print(truedmnumber)
        elif '万' in dmnumber:
            truedmnumber = float(dmnumber.replace('万', '')) * 10000
            # print(truedmnumber)
        else:
            truedmnumber = float(dmnumber.replace('', ''))
            # print(truedmnumber)

        # 硬币数
        coinnumber = str(soup.find_all('span', attrs={'id': 'v_ctimes'})[0].contents[0])
        # print(coinnumber)
        if '亿' in coinnumber:
            truecoinnumber = float(coinnumber.replace('亿', '')) * 100000000
            # print(truecoinnumber)
        elif '万' in coinnumber:
            truecoinnumber = float(coinnumber.replace('万', '')) * 10000
            # print(truecoinnumber)
        else:
            truecoinnumber = float(coinnumber.replace('', ''))
            # print(truecoinnumber)

        # 收藏数
        scnumber = str(soup.find_all('span', attrs={'id': 'stow_count'})[0].contents[0])
        # print(scnumber)
        if '亿' in scnumber:
            truescnumber = float(scnumber.replace('亿', '')) * 100000000
            # print(truescnumber)
        elif '万' in scnumber:
            truescnumber = float(scnumber.replace('万', '')) * 10000
            # print(truescnumber)
        else:
            truescnumber = float(scnumber.replace('', ''))
            # print(truescnumber)

        # 大分类
        bigtype = str(soup.find_all('a', attrs={'property': 'v:title'})[1].contents[0])
        # print(bigtype)

        # 小分类
        smalltype = str(soup.find_all('a', attrs={'property': 'v:title'})[2].contents[0])
        # print(smalltype)

        # 分享数
        sharenumber = str(soup.find_all('span', attrs={'class': 'num'})[0].contents[0])
        # print(sharenumber)
        if '亿' in sharenumber:
            truesharenumber = float(sharenumber.replace('亿', '')) * 100000000
            # print(truesharenumber)
        elif '万' in sharenumber:
            truesharenumber = float(sharenumber.replace('万', '')) * 10000
            # print(truesharenumber)
        else:
            truesharenumber = float(sharenumber.replace('', ''))
            # print(truesharenumber)

        # 标签
        tags = soup.find_all('li', attrs={'class': 'tag'})
        tagscontent = []
        # print(len(tags))
        for i in range(0, len(tags)):
            # print(tags[i].contents[0].contents[0])
            tagscontent.append(tags[i].contents[0].contents[0])
        truetagscontent = ','.join(tagscontent)
        # print(truetagscontent)

        # 视频描述
        description = str(soup.find_all('div', attrs={'id': 'v_desc'})[0].contents[0]).replace('\n', ' ')
        # print(description)

        saveData(avid, userid, title, uptime, truedjnumber, truedmnumber, truecoinnumber,
                 truescnumber, bigtype, smalltype, truesharenumber, truetagscontent, description)
    except Exception:
        pass

def saveData(avid, userid, title, uptime, truedjnumber, truedmnumber, truecoinnumber,
             truescnumber, bigtype, smalltype, truesharenumber, truetagscontent, description):
    try:
        cur = conn.cursor()
        cur.execute(
            "insert into bilibili_video(id, av_id, userid, av_title, uptime, djnumber, dmnumber, coinnumber, "
            "scnumber, bigtype, smalltype, sharenumber, tags, description)"
            "values(video_seq.Nextval, '%d', '%d', '%s', to_date('%s', 'yyyy-MM-dd hh24:mi'), '%f', '%f', '%f', "
            "'%f', '%s', '%s', '%f', '%s', '%s')"
            % (avid, userid, title, uptime, truedjnumber, truedmnumber, truecoinnumber,
            truescnumber, bigtype, smalltype, truesharenumber, truetagscontent, description))
        cur.execute("commit")
        # print('-------已插入数据库--------')
        print(avid)
        cur.close()

        if avid%100 == 0:
            msg = '已抓取并导入'+str(avid)+'条视频信息'
            sendMessage('Clannad', msg)
            print(msg)

    except Exception:
        pass


# 得到最大的uid
def getMaxUid():
    cursor.execute('select max(av_id) from bilibili_video')
    return cursor.fetchone()[0]


def sendMessage(replay_user, replay_content):
    bot = Bot(cache_path=True)  #设置登录缓存，不必每次运行都扫码

    # replay_user = u''  # 在这里写要回复的人
    # replay_content = u''  # 在这里写要回复的内容
    my_friend = ensure_one(bot.search(replay_user))
    my_friend.send(replay_content)


def main():
    start = getMaxUid()
    if start == None:  # 第一次抓取，指定uid
        start = 0
    print(start)
    print ("user start: ", start)
    stop = int(input("user stop: "))
    getSoup(start+1, stop)

    # print(soup)


if __name__=='__main__':
    main()




