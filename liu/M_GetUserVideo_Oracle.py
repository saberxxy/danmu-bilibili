#-*- coding=utf-8 -*-
# 抓取B站用户的投稿视频id，多进程并发版

"""
UID，用户名，视频数，视频aid
"""

from bs4 import BeautifulSoup
from urllib.parse import urlencode
from requests.exceptions import RequestException, HTTPError
from multiprocessing import Pool
from json import JSONDecodeError
from urllib import request
import cx_Oracle as cxo
import requests
import json
import time
import GetUsername

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
            print(" get aid error")
        finally:
            return count, aids


def main(number):
    try:
        username, uid = GetUsername.getUsername(number)  # 获取用户名, 用户ID
        get_video_uid = GetUserVideo(number)
        videonumber, aids = get_video_uid.get_aids()  # 获取视频id和视频数量
        aid = aids.strip()[:-1]  # 去掉末尾逗号

        saveData(uid, username, videonumber, aid)  # 插入数据库
    except HTTPError:
        print("error at userid: ", number)
        time.sleep(10)
        return main(number)
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
    finally:
        pool.close()
        pool.join()

    time2 = time.time()
    print((time2 - time1) / 60, u"分钟")