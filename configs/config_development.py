# -*- coding: utf-8 -*-
DEBUG=True
ENABLE_ROBOT = False

#保存登录的token
REDIS_HOST="192.168.33.10"
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=""

MYSQL_HOST = "192.168.33.10"
MYSQL_PORT = 3306
MYSQL_AUTOCOMMIT = True
MYSQL_CHARSET = 'utf8'
MYSQL_USER = "im"
MYSQL_PASSWD = "123456"
MYSQL_DATABASE = "gobelieve"
# host,port,user,password,db,auto_commit,charset
MYSQL = (MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DATABASE, MYSQL_AUTOCOMMIT, MYSQL_CHARSET)


GOBELIEVE_URL = "http://127.0.0.1"
#GOBELIEVE_URL = "http://api.gobelieve.io"

#客服app配置
APP_ID = 1453
APP_KEY = "xQrfaJPgfc5DsWuNUKcn4DMSWJUR4fcr"
APP_SECRET = 'ozj9rROFg3GmiqSa8kRBagNubf52BHlz'


