#-*- coding=utf-8 -*-
# 抓取B站用户投稿视频aid

import time
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from requests.exceptions import RequestException
from json import JSONDecodeError
from urllib import request
import cx_Oracle as cxo
import requests
import json
import random

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
        for number in range(start, stop + 1):
            url = 'http://space.bilibili.com/ajax/member/GetInfo'
            data = {
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

            r = requests.post(url, headers=headers, data=data)
            # print(r)
            userdata = json.loads(r.text)
            username = userdata.get('data').get('name') # 获取用户名
            uid = number  # number即为uid
            get_video_uid = GetUserVideo(number)
            videonumber, aids = get_video_uid.get_aids()  # 获取视频id和视频数量
            aid = aids.strip()[:-1] # 去掉末尾逗号
            saveData(uid, username, videonumber, aid)  # 插入数据库

            time.sleep(random.uniform(1, 5))  # 随机sleep
    except Exception:
        print("get page error: ", number)
        return getSoup(number + 1, stop + 1)


# 存入数据库
def saveData(uid, username, videonumber, aid):
    try:
        cur.execute("insert into bilibili_usertg(id ,userid, username, tgnumber, tgavid)"
                    "values(usertg_seq.Nextval, '%d', '%s', '%f', '%s')"
                    % (uid, username, videonumber, aid))
        cur.execute("commit")
        print('插入数据库:', username)
    except Exception:
        print("save error")


# 得到最大的uid
def getMaxUid():
    cur.execute('select max(userid) from bilibili_usertg')
    return cur.fetchone()[0]


class GetUserVideo(object):
    def __init__(self, mid):
        self._mid = mid

    def _getpage(self, page):
        data = {
            'mid': str(self._mid),
            'pagesize': '30',
            'tid': '0',
            'page': str(page),
            'keyword': '',
            'order': 'senddate',
            '_': '1496812411295'
        }
        # http://space.bilibili.com/ajax/member/getSubmitVideos?mid=15989779
        # &pagesize=30&tid=0&page=1&keyword=&order=senddate&_=1496812411295
        url = "http://space.bilibili.com/ajax/member/getSubmitVideos?" + urlencode(data)
        try:
            response = requests.get(url)
            if response.status_code != 200:
                return None
            html_cont = response.text
            return html_cont
        except RequestException:
            return None

    def _getinfo(self, cont):
        aids = ""
        try:
            data = json.loads(cont)
            if data and 'data' in data.keys():
                for video in data.get('data').get('vlist'):
                    aids = str(video.get('aid')) + ',' + aids
            return aids
        except JSONDecodeError:
            pass

    def _getpagenumber(self, cont):
        pages = 0
        count = 0
        try:
            data = json.loads(cont)
            if data and 'data' in data.keys():
                pages = data.get('data').get('pages')
                count = data.get('data').get('count')
        except JSONDecodeError:
            pass
        finally:
            return pages, count

    def get_aids(self):
        count = 0
        aids = ""
        try:
            pages, count = self._getpagenumber(self._getpage(1)) # 获取总页数和投稿视频数量
            if(pages != 0):
                for i in range(1, pages + 1):
                    aid = self._getinfo(self._getpage(i))
                    aids = aid + aids
        except Exception:
            print(" get aid error")
        finally:
            return count, aids


def main():
    time1 = time.time()

    try:
        start = getMaxUid()
        if start == None:
            start = 0
        stop = start + 100
        print(start, stop)
        getSoup(start+1, stop)
    finally:
        cur.close()
        conn.close()

    time2 = time.time()
    print((time2 - time1) / 60, u"分钟")


if __name__ == '__main__':
    main()