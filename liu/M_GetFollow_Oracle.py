#-*- coding=utf-8 -*-
# 抓取B站用户的关注id

"""
UID，用户名，关注数，关注用户UID
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

oracleHost = '127.0.0.1'
oracleUser = 'bilibili'
oraclePassword = '123456'
oracleDatabaseName = 'orcl'
oracleConn = oracleUser + '/' + oraclePassword + '@' + oracleHost + '/' + oracleDatabaseName
conn = cxo.connect(oracleConn)
cur = conn.cursor()


# 存入数据库
def saveData(uid, username, gznumber, gzsuserid):
    try:
        cur.execute("insert into bilibili_usergz(id ,userid, username, gznumber, gzsuserid)"
                    "values(usergz_seq.Nextval, '%d', '%s', '%f', '%s')"
                    % (uid, username, gznumber, gzsuserid))
        cur.execute("commit")
        print('插入数据库:', username)
    except Exception:
        print("save error")


# 得到最大的uid
def getMaxUid():
    cur.execute('select max(userid) from bilibili_usergz')
    return cur.fetchone()[0]


class GetFollowUid(object):
    def __init__(self, mid):
        self._follow_ids = ""
        self._mid = mid

    def _get_page(self, page_number):
        data = {
            'mid': str(self._mid),
            'page': str(page_number),
            '_': '1496211796946'
        }
        pages = 0
        follownumber = 0
        follow_ids = ""
        try:
            # url
            # http://space.bilibili.com/ajax/friend/GetAttentionList?mid=12266&page=1&_=1496211796946
            url = "http://space.bilibili.com/ajax/friend/GetAttentionList?" + urlencode(data)
            # print(url)
            # 请求网页
            response = requests.get(url)
            if response.status_code != 200:
                return None
            html_cont = response.text
            try:
                data = json.loads(html_cont)
                if data and (data.get('status') is True):
                    if data and 'data' in data.keys():
                        if(page_number == 1):
                            pages = data.get('data').get('pages')
                            follownumber = data.get('data').get('results')
                        for follow in data.get('data').get('list'):
                            follow_ids = str(follow.get('fid')) + ',' + follow_ids
                elif (data.get('data') == "关注列表中没有值"):
                    pages = 0
                    follownumber = 0
            except JSONDecodeError:
                pass
            self._follow_ids = follow_ids + self._follow_ids
            # print(self._follow_ids)
            return pages, follownumber
        except RequestException:
            return self._get_page(page_number)

    def get_uids(self):
        follownumber = 0
        try:
            pages, follownumber = self._get_page(1)# 获取总页数和关注数量
            if(follownumber != 0):# 关注数量不为0就开始爬取
                if(pages < 6): # 不超过5页
                    for i in range(2, pages + 1):
                        self._get_page(i)
                else:
                    for i in range(2, 6):#超过5页，暂且先爬取前五页
                        self._get_page(i)
        except Exception:
            print(" get uid error")
        finally:
            return self._follow_ids, follownumber


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
        get_gz_uid = GetFollowUid(number)
        gzsuid, gznumber = get_gz_uid.get_uids()  # 获取关注id和关注数量
        gzsuid = gzsuid.strip()[:-1]

        saveData(uid, username, gznumber, gzsuid)  # 插入数据库
    except Exception:
        pass


if __name__ == '__main__':
    time1 = time.time()

    start = getMaxUid()  # 抓取范围
    stop = start + 1000
    print(start, stop)

    try:
        pool = Pool(processes=10)  # 设定并发进程的数量
        pool.map(main, (i for i in range(start, stop + 1)))
    except Exception:
        pass

    time2 = time.time()
    print((time2 - time1) / 60, u"分钟")

