#-*- coding=utf-8 -*-

import urllib
import urllib.request
import re
from io import BytesIO
import gzip
import zlib
import time
from datetime import datetime
import pymysql
from bs4 import BeautifulSoup
import socket

socket.setdefaulttimeout(20)

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

mysql_host = "localhost"
mysql_port = 3306
mysql_user = "root"
mysql_pwd = "root"
mysql_db = "test"  #数据库名
mysql_tb = "danmu"  #表名

# 得到最大的id
def getMaxId():
    conn = None
    cur = None
    try:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_pwd, port=mysql_port, db=mysql_db, charset="utf8")
        cur = conn.cursor()

        cur.execute('select max(id) from test.danmu;')
        return cur.fetchone()[0]
    except Exception:
        print ("Mysql Error %d: %s" % (Exception.args[0], Exception.args[1]))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# 保存数据
def saveData(cmd, data):
    conn = None
    cur = None
    try:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_pwd, port=mysql_port, db=mysql_db, charset="utf8")
        cur = conn.cursor()
        for i in data:
            try:
                cmdline = cmd % i
                cur.execute(cmdline)
            except Exception:
                print (cmdline, str(Exception))
                open("error.log", "a").write("\n%s\n %s\n" % (cmdline, str(Exception)))
        conn.commit()
    except Exception:
        print ("Mysql Error %d: %s" % (Exception.args[0], Exception.args[1]))
        print (cmd % data[0])
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


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
            print ("get error: %s" % str(Exception))


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
        title = ""
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
        cmd = """insert into test.danmu (show_time, direc, font_size, locate, post_time, style, color, danmu_id, content, av_id, av_title) values (%s,%s,%s,%s,'%s',%s,'%s',%s,'%s',%s,'%s');"""
        for item in root.findall("d"):
            p = item.get("p").split(",")
            content = item.text and pymysql.escape_string(item.text) or ""
            p.append(content)
            p.append(str(av_id))
            p.append(pymysql.escape_string(av_title))
            p[4] = datetime.utcfromtimestamp(int(p[4]))
            data.append(tuple(p))
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
            print (av_id, getMaxId())
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
    conn = None
    cur = None
    conn = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_pwd, port=mysql_port, db=mysql_db, charset="utf8")
    cur = conn.cursor()

    cur.execute('select max(av_id) from test.danmu;')
    return cur.fetchone()[0]

def main():
    startTime = time.clock()
    start = getMaxAvId()
    if start == None:  # 第一次抓取，指定av号
        start = 1
    print ("av start: ", start)
    stop = int(input("av stop: "))

    for i in range(start+1, stop+1):
        saveDanmu(i)
    stopTime = time.clock()
    print ((stopTime - startTime)/60,)
    print ("mins")


if __name__ == '__main__':
    main()



