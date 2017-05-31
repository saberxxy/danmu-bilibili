#-*- coding=utf-8 -*-
# 抓取B站用户的粉丝id

"""
UID，用户名，粉丝数，粉丝UID
"""

import cx_Oracle as cxo
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import GetFansUid

oracleHost = '127.0.0.1'
oracleUser = 'bilibili'
oraclePassword = '123456'
oracleDatabaseName = 'orcl'
oracleConn = oracleUser + '/' + oraclePassword + '@' + oracleHost + '/' + oracleDatabaseName
conn = cxo.connect(oracleConn)
cur = conn.cursor()


# 获取用户网页数据
def getSoup(start, stop):

    try:
        for number in range(start, stop+1):

            url = 'http://space.bilibili.com/'+str(number)+'/#!/'
            # url = 'http://space.bilibili.com/122879/#!/'

            # "http://http://space.bilibili.com/122879/#!/"
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
            )
            dcap["phantomjs.page.settings.loadImages"] = False  #不加载图片，加快速度
            # executable_path='D:\\Chrome\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe',
            driver = webdriver.PhantomJS(desired_capabilities=dcap)
            driver.get(url)
            content = driver.page_source  # 获取网页内容
            # print(content)
            driver.close()
            soup = BeautifulSoup(content, 'lxml')
            username= getInfo(soup) # 获取用户名
            uid = number # number即为uid

            get_fans_uid = GetFansUid.GetFansUid(number)
            fansuid, fansnumber = get_fans_uid.get_uids()  # 获取粉丝id和粉丝数量
            print(uid, username, fansnumber)

            saveData(uid, username, fansnumber, fansuid)# 插入数据库
    except Exception:
        print("get page error")
        return getSoup(number + 1, stop+1)


# 提取信息
def getInfo(soup):

    try:
        # 用户名
        username = str(soup.find_all(attrs={'id': 'h-name'})[0].contents[0])
        print(username)

        return username
    except Exception:
        print("get info error")


# 存入数据库
def saveData(uid, username, fansnumber, fansuserid):

    try:
        cur.execute("insert into bilibili_userfans(id ,userid, username, fansnumber, fansuserid)"
                    "values(userfans_seq.Nextval, '%d', '%s', '%f', '%s')"
                    % (uid, username, fansnumber, fansuserid))
        cur.execute("commit")
        print('插入数据库:', username)
        # cur.execute("select username, fansnumber from bilibili_userfans order by id DESC")
        # fan = cur.fetchone()
        # print(fan[0])
    except Exception:
        print("save error")


# 得到最大的uid
def getMaxUid():
    cur.execute('select max(userid) from bilibili_userfans')
    return cur.fetchone()[0]


def main():
    try:
        getSoup(122910, 122979)
    finally:
        cur.close()
        conn.close()


if __name__=='__main__':
    main()