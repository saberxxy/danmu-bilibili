#-*- coding=utf-8 -*-
# 抓取B站粉丝uid

from urllib.parse import urlencode
from requests.exceptions import RequestException
from json import JSONDecodeError
import requests
import json


class GetFansUid(object):
    def __init__(self, mid):
        self._fans_ids = ""
        self._mid = mid

    def _get_page(self, page_number):
        data = {
            'mid': str(self._mid),
            'page': str(page_number),
            '_': '1496132105785'
        }
        pages = 0
        fansnumber = 0
        fans_ids = ""
        try:
            # url
            # url = "http://space.bilibili.com/'+str(number)+'/#!/fans/fans"
            # http://space.bilibili.com/ajax/friend/GetFansList?mid=122879&page=4&_=1496132105785
            url = "http://space.bilibili.com/ajax/friend/GetFansList?" + urlencode(data)
            # print(url)
            # 请求网页
            response = requests.get(url)
            # print(response.status_code)
            if response.status_code != 200:
                return None
            html_cont = response.text
            try:
                data = json.loads(html_cont)
                if data and (data.get('status') is True):
                    if data and 'data' in data.keys():
                        if(page_number == 1):
                            pages = data.get('data').get('pages')
                            # print(pages)
                            fansnumber = data.get('data').get('results')
                            # print(fansnumber)
                        for fans in data.get('data').get('list'):
                            fans_ids = str(fans.get('fid')) + ',' + fans_ids
                elif (data.get('data') == "粉丝列表中没有值"):
                    # print("status :", data.get('status'))
                    pages = 0
                    fansnumber = 0
            except JSONDecodeError:
                pass
            self._fans_ids = fans_ids + self._fans_ids
            # print(self._fans_ids)
            return pages, fansnumber
        except RequestException:
            return self._get_page(page_number)

    def get_uids(self):
        fansnumber = 0
        try:
            pages, fansnumber = self._get_page(1)# 获取总页数和粉丝数量
            if(fansnumber != 0):# 粉丝数量不为0就开始爬取
                if(pages < 6): # 不超过5页
                    for i in range(2, pages + 1):
                        self._get_page(i)
                else:
                    for i in range(2, 6):#超过5页，暂且先爬取前五页
                        self._get_page(i)
        except Exception:
            print(" get uid error")
        finally:
            return self._fans_ids, fansnumber


# def main():
#     get_fans_uid = GetFansUid(122883)
#     fans_ids, fansnumber= get_fans_uid.get_uids()
#     print("fans number:", fansnumber)
#     print("fans id:", fans_ids)
#
#
# if __name__ == '__main__':
#     main()