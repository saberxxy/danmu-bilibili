#-*- coding=utf-8 -*-
# 清洗视频信息
# 对从niconico视频网上链接的视频描述去除标签，只保留niconico编号

import cx_Oracle as cxo
import re

oracleHost = '127.0.0.1'
oraclePort = '1521'
oracleUser = 'bilibili'
oraclePassword = '123456'
oracleDatabaseName = 'orcl'
oracleConn = oracleUser + '/' + oraclePassword + '@' + oracleHost + '/' + oracleDatabaseName
conn = cxo.connect(oracleConn)
cursor = conn.cursor()


cursor.execute('select av_id, description from bilibili_video')
content = cursor.fetchall()
for i in content:
    # print(list(i)[-1])
    if 'onmouseout=' in list(i)[-1]:
        a = str(re.findall(r'.*target="_blank">(.*)<img.*', list(i)[1])[0])
        b = int(list(i)[0])  # av号
        print(a, b)
        cursor.execute("update bilibili_video set description='%s' where av_id='%d'"
                       % (a, b))
        cursor.execute("commit")