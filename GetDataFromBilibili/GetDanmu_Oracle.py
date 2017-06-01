#-*- coding=utf-8 -*-
# 获取弹幕

import urllib
import urllib.request
import re
from io import BytesIO
import gzip
import zlib
import time
from datetime import datetime
from bs4 import BeautifulSoup
import socket
import cx_Oracle as cxo


socket.setdefaulttimeout(20)

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


oracleHost = '127.0.0.1'
oraclePort = '1521'
oracleUser = 'bilibili'
oraclePassword = '123456'
oracleDatabaseName = 'orcl'
oracleConn = oracleUser + '/' + oraclePassword + '@' + oracleHost + '/' + oracleDatabaseName
conn = cxo.connect(oracleConn)
cursor = conn.cursor()



# 保存数据
def saveData(cmd, data):

    cur = conn.cursor()
    try:
        for i in data:
            cmdline = cmd % i
            # print(cmdline)
            cur.execute(str(cmdline))
            cur.execute("commit")
    except Exception:
        pass



# 处理gzip压缩后的网页
def gzipDecode(zipData):
    try:
        buf = BytesIO(zipData)
        http_page = gzip.GzipFile(fileobj=buf).read()
        return http_page.decode("utf-8")
    except Exception:
        pass


# 获取链接
def getUrl(url):

    while True:
        try:
            http_page = gzipDecode(camouflageBrowser(url))
            return http_page
        except Exception:
            pass



# 解决分P问题,拿到分P或不分P的所有cid和标题
def fetchCidsFromHtml(avid):

    def getCid(url):
        try:
            http_page = getUrl(url)
            cid = re.findall(r"cid=(\d+)", http_page)
            cid = cid and cid[0] or ""
            return cid
        except Exception:
            pass


    url = "http://www.bilibili.com/video/av%s/" % str(avid)
    http_page = getUrl(url)
    title = ""

    try:
        soup = BeautifulSoup(http_page, "html.parser")
        title_div = soup.findAll('div', attrs={'class': 'v-title'})
        title_div = title_div and title_div[0] or None
        page_opt = soup.find("select", attrs={"id": "dedepagetitles"})
        if page_opt:
            # 处理分P问题
            return [{"cid": getCid("http://www.bilibili.com%s" % item.get("value")), "title": item.text} for item in page_opt.findAll("option")]
        if title_div:
            title = title_div.find('h1').text
    except Exception:
        pass

    cid = re.findall(r"cid=(\d+)", http_page)
    cid = cid and cid[0] or ""
    return [{"cid": cid, "title": title}]


#  获取弹幕XML文件
def getDanmu(cid):
    if not cid:
        return "未找到弹幕"
    try:
        cid_url = "http://comment.bilibili.com/%s.xml" % cid
        danmu_xml = urllib.request.urlopen(cid_url).read()
        xml = zlib.decompressobj(-zlib.MAX_WBITS).decompress(danmu_xml).decode()  # 返回解压后的数据

        return xml  # 删除换行符
    except Exception:
        pass




# 根据xml格式的字符串提取数据并格式化
def formatData(av_id, av_title, xml_str):

    try:

        xml_str = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u"", xml_str)

        root = ET.fromstring(xml_str)
        data = []
        cmd = """insert into bilibili_danmu (id, show_time, direc, font_size, locate, post_time, style, color, danmu_id, content, av_id, av_title) values (danmu_seq.Nextval, '%f', '%f', '%f', '%f', to_date('%s', 'yyyy-MM-dd hh24:mi:ss'), '%s', '%s', '%d', '%s', %d, '%s')"""
        for item in root.findall("d"):
            a = []
            p = item.get("p").split(",")
            a.append(float(p[0]))
            a.append(float(p[1]))
            a.append(float(p[2]))
            a.append(float(p[3]))
            a.append(p[4])
            a.append(float(p[5]))
            a.append(str(p[6]))
            a.append(int(p[7]))
            content = item.text
            a.append(content)
            a.append(int(av_id))
            a.append(av_title)

            a[4] = datetime.utcfromtimestamp(int(a[4]))
            data.append(tuple(a))

        return cmd, data

    except Exception:
        pass



# 保存弹幕
def saveDanmu(av_id):
    try:
        for item in fetchCidsFromHtml(av_id):
            xml_data = getDanmu(item.get("cid"))
            if xml_data == "未找到弹幕":
                continue
            cmd, data = formatData(av_id, item.get("title"), xml_data)

            saveData(cmd, data)
            print(av_id, getCount())
    except Exception:
        pass



# 迭代抓取并写入文件
def getWrite(start, stop):
    for i in range(start, stop+1):  # 迭代抓取
        xml = getDanmu(i)
        a = 'E:\\Program\\XML\\danmuXML\\av' + str(i) + '.xml'
        open(a, 'w').write("".join(xml.splitlines()))
        print (i)  # 写入文件后打印，表示抓取完成


# 伪装成浏览器
def camouflageBrowser(url):
    myHeaders = [
				  "Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0",
			  	  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36",
			      "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0",
			      "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
			      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.5 Safari/536.11"
				 ]  # 添加请求头
    try:
        content = urllib.request.urlopen(url).read()
        return content
    except Exception:
        pass


# 分P视频抓取测试
def test():
    saveDanmu(2063787)
    saveDanmu(6540)


# 得到最大的av_id
def getMaxAvId():
    cursor.execute('select max(av_id) from bilibili_danmu')
    return cursor.fetchone()[0]


# 取得弹幕数量
def getCount():
    cursor.execute('select count(1) from bilibili_danmu')
    return cursor.fetchone()[0]


def main():
    startTime = time.clock()
    start = getMaxAvId()
    if start == None:  # 第一次抓取，指定av号
        start = 1
    # print(start)
    print ("av start: ", start)
    stop = int(input("av stop: "))

    # print(123)

    for i in range(start+1, stop+1):
        saveDanmu(i)
        # print(i)
    stopTime = time.clock()
    print ((stopTime - startTime)/60,)
    print ("mins")



if __name__ == '__main__':
    main()



