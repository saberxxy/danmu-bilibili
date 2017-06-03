#-*- coding=utf-8 -*-
# 抓取B站视频信息

"""
av号，up主userid，视频标题，发布时间，大分类，小分类，标签，视频描述，点击数，弹幕数，硬币数，收藏数，分享数，评论数，最高日排名
"""

import urllib
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from io import BytesIO
import gzip
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import re
import cx_Oracle as cxo
from urllib.parse import urlencode
import requests
import json

oracleHost = '127.0.0.1'
oraclePort = '1521'
oracleUser = 'bilibili'
oraclePassword = '123456'
oracleDatabaseName = 'orcl'
oracleConn = oracleUser + '/' + oraclePassword + '@' + oracleHost + '/' + oracleDatabaseName
conn = cxo.connect(oracleConn)
cursor = conn.cursor()


def getSoup(start, stop):
    try:
        for number in range(start, stop + 1):
            url1 = 'http://www.bilibili.com/video/av' + str(number) + '/'
            data1 = {}
            params = urllib.parse.urlencode(data1).encode(encoding='UTF8')
            req = urllib.request.Request("%s?%s" % (url1, params))
            headers = {
                'User-Agent': "ozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                'Referer': 'http://www.bing.com/'
            }
            for i in headers:
                req.add_header(i, headers[i])

            content = urllib.request.urlopen(url1).read()
            buf = BytesIO(content)
            http_page = gzip.GzipFile(fileobj=buf).read().decode("utf-8")
            soup = BeautifulSoup(http_page, "html.parser")
            # print(soup)


            data2 = {
                'aid': str(number),
            }
            url2 = 'http://api.bilibili.com/archive_stat/stat?callback=jQuery17202479039144368551_1496476516783&' + urlencode(
                data2) + '&type=jsonp&_=1496476517124'
            # print(url2)
            response = requests.get(url2)
            html_cont = response.text
            json1 = json.loads(re.match(".*?({.*}).*", html_cont, re.S).group(1))
            # print(json1)
            jasondata = json1['data']
            # print(jasondata)

            getInfo(soup, jasondata)

    except Exception:
        pass

def getInfo(soup, jasondata):
    try:
        # av号
        avid = int(re.findall(r'.*aid=(.*)">.*', str(soup.find_all('span', attrs={'class': 't fav_btn'})[0]))[0])
        print(avid)
        # up主userid
        userid = int(re.findall(r'.*mid="(.*)">.*', str(soup.find_all('div', attrs={'class': 'upinfo'})[0]))[-1])
        print(userid)
        # 视频标题
        title = str(soup.find_all('div', attrs={'class': 'v-title'})[0].contents[0].contents[0])
        print(title)
        # 发布时间
        uptime = str(soup.find_all('time', attrs={'itemprop': 'startDate'})[0].contents[0].contents[0])
        print(uptime)
        # 大分类
        bigtype = str(soup.find_all('a', attrs={'property': 'v:title'})[1].contents[0])
        print(bigtype)
        # 小分类
        smalltype = str(soup.find_all('a', attrs={'property': 'v:title'})[2].contents[0])
        print(smalltype)
        # 标签
        tags = soup.find_all('a', attrs={'class': 'tag-val'})
        # print(tags)
        tagscontent = []
        for i in range(0, len(tags)):
            # print(tags[i].contents[0].contents[0])
            tagscontent.append(tags[i].contents[0])
        truetagscontent = ','.join(tagscontent)
        print(truetagscontent)
        # 视频描述
        description = str(soup.find_all('div', attrs={'id': 'v_desc'})[0].contents[0]).replace('\n', ' ')
        print(description)

        # 点击数
        djnumber = int(jasondata['view'])
        print(djnumber)
        # 弹幕数
        dmnumber = int(jasondata['danmaku'])
        print(dmnumber)
        # 硬币数
        coinnumber = int(jasondata['coin'])
        print(coinnumber)
        # 收藏数
        scnumber = int(jasondata['favorite'])
        print(scnumber)
        # 分享数
        sharenumber = int(jasondata['share'])
        print(sharenumber)
        # 评论数
        commentnumber = int(jasondata['reply'])
        print(commentnumber)
        # 最高日排名
        hisrank = int(jasondata['his_rank'])
        print(hisrank)

        print('--------------------------------------')

        saveData(avid, userid, title, uptime, bigtype, smalltype, truetagscontent, description,
                 djnumber, dmnumber, coinnumber, scnumber,  sharenumber, commentnumber, hisrank)

    except Exception:
        pass

def saveData(avid, userid, title, uptime, bigtype, smalltype, truetagscontent, description,
                 djnumber, dmnumber, coinnumber, scnumber,  sharenumber, commentnumber, hisrank):
    try:
        cur = conn.cursor()
        cur.execute(
            "insert into bilibili_video(id, av_id, userid, av_title, uptime, bigtype, smalltype, tags, description, "
            "djnumber, dmnumber, coinnumber, scnumber, sharenumber, commentnumber, hisrank )"
            "values(video_seq.Nextval, '%d', '%d', '%s', to_date('%s', 'yyyy-MM-dd hh24:mi'), '%s', '%s', '%s', '%s', "
            "'%d', '%d', '%d', '%d', '%d', '%d', '%d')"
            % (avid, userid, title, uptime, bigtype, smalltype, truetagscontent, description,
                 djnumber, dmnumber, coinnumber, scnumber,  sharenumber, commentnumber, hisrank))
        cur.execute("commit")
        # print('-------已插入数据库--------')
        print(avid)
        cur.close()

        # if avid%100 == 0:
        #     msg = '已抓取并导入'+str(avid)+'条视频信息'
        #     SendMessage.sendMessage('东京中央软体产业株式会社', msg)
        #     # sendMessage('东京中央软体产业株式会社', msg)
        #     print(msg)

    except Exception:
        pass

# 得到最大的uid
def getMaxUid():
    cursor.execute('select max(av_id) from bilibili_video')
    return cursor.fetchone()[0]

def main():
    start = getMaxUid()
    if start == None:  # 第一次抓取，指定uid
        start = 0
    print ("user start: ", start)
    stop = start+100
        # int(input("user stop: "))
    getSoup(start+1, stop)


    # print(soup)


if __name__=='__main__':
    main()




