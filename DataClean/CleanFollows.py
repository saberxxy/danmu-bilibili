#-*- coding=utf-8 -*-
# 清洗关注信息
# 去掉关注列表末尾的逗号

import re
import cx_Oracle as cxo

oracleHost = '127.0.0.1'
oraclePort = '1521'
oracleUser = 'bilibili'
oraclePassword = '123456'
oracleDatabaseName = 'orcl'
oracleConn = oracleUser + '/' + oraclePassword + '@' + oracleHost + '/' + oracleDatabaseName
conn = cxo.connect(oracleConn)
cursor = conn.cursor()

cursor.execute('select userid, gzsuserid from bilibili_usergz')
content = cursor.fetchall()

for i in content:
    # print(list(i)[-1])
    if list(i)[-1] != None:
        a = list(i)[-1]  # 原始关注列表
        gzslist = re.compile(r',$').sub('', a)  # 去掉末尾逗号的关注列表
        # print(m)
        # print(a)
        userid = int(list(i)[0])  # userid
        # print(b)
        print(userid, gzslist)
        cursor.execute("update bilibili_usergz set gzsuserid='%s' where userid='%d'"
                       % (gzslist, userid))
        cursor.execute("commit")