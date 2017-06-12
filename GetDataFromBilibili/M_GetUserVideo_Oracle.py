#-*- coding=utf-8 -*-
# 抓取B站用户的投稿视频id，多进程并发版

"""
UID，用户名，视频数，视频aid
"""

from bs4 import BeautifulSoup
from urllib.parse import urlencode
from requests.exceptions import RequestException
from multiprocessing import Pool
from json import JSONDecodeError
from urllib import request
import cx_Oracle as cxo
import requests
import json
import time
import urllib.parse
import random

oracleHost = '127.0.0.1'
oracleUser = 'bilibili'
oraclePassword = '123456'
oracleDatabaseName = 'orcl'
oracleConn = oracleUser + '/' + oraclePassword + '@' + oracleHost + '/' + oracleDatabaseName
conn = cxo.connect(oracleConn)
cur = conn.cursor()


# 存入数据库
def saveData(uid, username, videonumber, aid):
    try:
        cur.execute("insert into bilibili_usertg(id ,userid, username, tgnumber, tgavid)"
                    "values(usertg_seq.Nextval, '%d', '%s', '%f', '%s')"
                    % (uid, username, videonumber, aid))
        cur.execute("commit")
        # print('插入数据库:', username)
        print(uid)
    except Exception:
        # print("save error")
        pass

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
        tag_ids = ""
        tag_names = ""
        tag_counts = ""
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
            # print(" get aid error")
            pass
        finally:
            return count, aids


def main(number):
    try:
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
        username = userdata.get('data').get('name')  # 获取用户名
        uid = number  # number即为uid
        get_video_uid = GetUserVideo(number)
        videonumber, aids = get_video_uid.get_aids()  # 获取视频id和视频数量
        aid = aids.strip()[:-1]  # 去掉末尾逗号

        saveData(uid, username, videonumber, aid)  # 插入数据库
        time.sleep(random.uniform(1, 5))  # 更据动态网页加载耗时，此处为随机时间
    except Exception:
        # print("error at userid: ", number)
        pass


if __name__ == '__main__':
    time1 = time.time()

    start = getMaxUid()  # 抓取范围
    stop = start + 100
    print(start, stop)

    try:
        pool = Pool(processes=10)  # 设定并发进程的数量
        pool.map(main, (i for i in range(start+1, stop+1)))
    except Exception:
        pass

    time2 = time.time()
    print((time2 - time1) / 60, u"分钟")