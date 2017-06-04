#-*- coding=utf-8 -*-
# 抓取B站用户信息

import json
import datetime
import random
from multiprocessing import Pool
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import cx_Oracle as cxo
import SendMessage
import urllib
import urllib.request
import os
import urllib.request
import urllib.parse
from io import BytesIO
import gzip
import requests
from urllib.parse import urlencode
import time

oracleHost = '127.0.0.1'
oraclePort = '1521'
oracleUser = 'bilibili'
oraclePassword = '123456'
oracleDatabaseName = 'orcl'
oracleConn = oracleUser + '/' + oraclePassword + '@' + oracleHost + '/' + oracleDatabaseName
conn = cxo.connect(oracleConn)
cursor = conn.cursor()


def getInfo(jsondata1, jsondata2):

    list = []

    try:
        # userid
        userid = int(jsondata2['mid'])
        list.append(userid)
        # print('userid', userid)
    except Exception:
        pass

    try:
        # 用户名
        username = str(jsondata2['name'])
        list.append(username)
        # print('用户名', username)
    except Exception:
        pass

    try:
        # 注册时间
        time1 = jsondata2['regtime']
        time2 = time.localtime(time1)
        regtime = str(time.strftime('%Y-%m-%d %H:%M:%S', time2))
        list.append(regtime)
        # print('注册时间', regtime)
    except Exception:
        list.append('')
        pass

    try:
        # 生日
        birthday = str(jsondata2['birthday'])
        list.append(birthday[5:10])
        # print('生日', birthday)
    except Exception:
        list.append('')
        pass

    try:
        # 地区
        geo = str(jsondata2['place'])
        list.append(geo)
        # print('地区', geo)
    except Exception:
        list.append('')
        pass

    try:
        # 性别
        sex = str(jsondata2['sex'])
        list.append(sex)
        # print('性别', sex)
    except Exception:
        list.append('')
        pass

    try:
        # 粉丝数
        fansnumber = int(jsondata2['fans'])
        list.append(fansnumber)
        # print('粉丝数', fansnumber)
    except Exception:
        pass

    try:
        # 关注数
        gznumber = int(jsondata2['friend'])
        list.append(gznumber)
        # print('关注数', gznumber)
    except Exception:
        pass

    try:
        # 播放数
        bfnumber = int(jsondata2['playNum'])
        list.append(bfnumber)
        # print('播放数', bfnumber)
    except Exception:
        pass

    try:
        # 投稿视频数
        videonumber = int(jsondata1['video'])
        list.append(videonumber)
        # print('投稿数', videonumber)
    except Exception:
        pass

    try:
        # 是否认证
        approve = str(jsondata2['approve'])
        list.append(approve)
        # print('是否认证', approve)
    except Exception:
        pass

    try:
        # 用户等级
        userlevel = int(jsondata2['level_info']['current_level'])
        list.append(userlevel)
        # print('用户等级', userlevel)
    except Exception:
        pass

    try:
        # 用户签名
        sign = str(jsondata2['sign'])
        list.append(sign)
        # print('用户签名', sign)
    except Exception:
        list.append('')
        pass

    # print('------------------------')
    # print(list)
    # print(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7],
    #       list[8], list[9], list[10], list[11], list[12])

    try:
        saveData(list[0], list[1], list[2], list[3], list[4], list[5],
             list[6], list[7], list[8], list[9],
             list[10], list[11], list[12])

        time.sleep(random.uniform(1, 5))  # 更据动态网页加载耗时，此处为随机时间
    except Exception:
        pass



def saveData(userid, username, regtime, birthday, geo, sex,
            fansnumber, gznumber, bfnumber, videonumber,
            approve, userlevel, sign):
    try:
        cur = conn.cursor()
        cur.execute(
            "insert into bilibili_user(id, userid, username, regtime, birthday, geo, sex,  "
            "fansnumber, gznumber, bfnumber, videonumber, "
            "approve, userlevel, sign )"
            "values(user_seq.Nextval, '%d', '%s', to_date('%s', 'yyyy-MM-dd hh24:mi:ss'), "
            "to_date('%s', 'MM-dd'), '%s', '%s', "
            "'%d', '%d', '%d', '%d', "
            "'%s', '%d', '%s')"
            % (userid, username, regtime, birthday, geo, sex,
               fansnumber, gznumber, bfnumber, videonumber,
               approve, userlevel, sign))
        cur.execute("commit")
        # print('-------已插入数据库--------')
        print(userid)
        cur.close()
    except Exception:
        pass

# 得到最大的uid
def getMaxUid():
    cursor.execute('select max(userid) from bilibili_user')
    return cursor.fetchone()[0]


def main(number):
    try:
        # 获取投稿数
        url1 = 'http://space.bilibili.com/ajax/member/getNavNum?mid=' + str(number) + '&_=1496544951986'
        req = requests.get(url1)
        jsondata1 = json.loads(re.match(".*?({.*}).*", req.text, re.S).group(1))['data']

        # 获取其余信息
        url2 = 'http://space.bilibili.com/ajax/member/GetInfo'
        data2 = {
            'mid': '{}'.format(number),
            'csrf': ''
        }
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '32',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'UM_distinctid=15b9449b43c1-04dfdd66b40759-51462d15-1fa400-15b9449b43d83; fts=1492841510; sid=j4j61vah; purl_token=bilibili_1492841536; buvid3=30EA0852-5019-462F-B54B-1FA471AC832F28080infoc; rpdid=iwskokplxkdopliqpoxpw; _cnt_pm=0; _cnt_notify=0; _qddaz=QD.cbvorb.47xm5.j1t4z5yc; pgv_pvi=9558976512; pgv_si=s2784223232; _dfcaptcha=02d046fd3cc2bfd2ce6724f8b2185887; CNZZDATA2724999=cnzz_eid%3D1176255236-1492841785-http%253A%252F%252Fspace.bilibili.com%252F%26ntime%3D1492857985',
            'Host': 'space.bilibili.com',
            'Origin': 'http://space.bilibili.com',
            'Referer': 'http://space.bilibili.com/{}/'.format(number),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        r = requests.post(url2, headers=headers, data=data2)
        # print(r)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        jsondata2 = json.loads(re.match(".*?({.*}).*", r.text, re.S).group(1))['data']

        getInfo(jsondata1, jsondata2)
    except Exception:
        pass


if __name__ == '__main__':
    time1 = time.time()

    start = getMaxUid()  # 抓取范围
    stop = start + 1000
    print(start, stop)

    try:
        pool = Pool(processes=10)  # 设定并发进程的数量
        pool.map(main, (i for i in range(start+1, stop+1)))
    except Exception:
        pass

    time2 = time.time()
    print((time2 - time1) / 60, u"分钟")


