#-*- coding=utf-8 -*-
# 清洗粉丝信息
# 去掉粉丝列表末尾的逗号

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

cursor.execute('select userid, fansuserid from bilibili_userfans')
content = cursor.fetchall()

for i in content:
    # print(list(i)[-1])
    if list(i)[-1] != None:
        a = list(i)[-1]  # 原始粉丝列表
        fanslist = re.compile(r',$').sub('', a)  # 去掉末尾逗号的粉丝列表
        # print(m)
        # print(a)
        userid = int(list(i)[0])  # userid
        # print(b)
        print(fanslist, userid)
        cursor.execute("update bilibili_userfans set fansuserid='%s' where userid='%d'"
                       % (fanslist, userid))
        cursor.execute("commit")
