# -*- coding: utf-8 -*-
DEBUG=True
ENABLE_ROBOT = False

#保存登录的token
REDIS_HOST="127.0.0.1"
REDIS_PORT=6378
REDIS_DB=1


#读取客服的用户名和密码
MYSQL_HOST = "10.251.43.254"
MYSQL_PORT = 3306
MYSQL_AUTOCOMMIT = True
MYSQL_CHARSET = 'utf8'
MYSQL_USER = "im"
MYSQL_PASSWD = "123456"
MYSQL_DATABASE = "gobelieve"
# host,port,user,password,db,auto_commit,charset
MYSQL = (MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DATABASE, MYSQL_AUTOCOMMIT, MYSQL_CHARSET)

#获取gobelieve的token
GOBELIEVE_URL = "http://api.gobelieve.io"

#客服app配置
APP_ID = 1670
APP_KEY = "9xgK0dEMM0L3Zt7m11ZBcPRB6WlvjhAo"
APP_SECRET = "LlCTMpnP9fW9nU9LUxySPs7gFJoIOe1P"

