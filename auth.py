# -*- coding: utf-8 -*-
from flask import request, Blueprint
import random
import json
import time
import requests
import urllib
import logging
import base64
from datetime import datetime
from functools import wraps
from util import make_response
from model import code
from model import token
from model import user
from authorization import create_token
from authorization import login_gobelieve
import config

app = Blueprint('auth', __name__)
rds = None


def INVALID_PARAM():
    e = {"error":"非法输入"}
    logging.warn("非法输入")
    return make_response(400, e)


def INVALID_USER():
    e = {"error":"非法的用户名"}
    logging.warn("非法的用户名")
    return make_response(400, e)
    
def INVALID_REFRESH_TOKEN():
    e = {"error":"非法的refresh token"}
    logging.warn("非法的refresh token")
    return make_response(400, e)
 
    
def CAN_NOT_GET_TOKEN():
    e = {"error":"获取imsdk token失败"}
    logging.warn("获取imsdk token失败")
    return make_response(400, e)
   

def test_user_id(username):
    max_int = (1<<63) - 1
    uid = max_int - (ord(username[10]) - ord('0'))
    return uid

def is_test_user(number):
    if number == "13800000000@gobelieve.io" or \
       number == "13800000001@gobelieve.io" or \
       number == "13800000002@gobelieve.io" or \
       number == "13800000003@gobelieve.io" or \
       number == "13800000004@gobelieve.io" or \
       number == "13800000005@gobelieve.io" or \
       number == "13800000006@gobelieve.io" or \
       number == "13800000007@gobelieve.io" or \
       number == "13800000008@gobelieve.io" or \
       number == "13800000009@gobelieve.io" :
        return True
    else:
        return False

    
@app.route("/auth/token", methods=["POST"])
def access_token():
    if not request.data:
        return INVALID_PARAM()

    obj = json.loads(request.data)
    username = obj["username"]
    password = obj["password"]
    if is_test_user(username) and password == "11111111":
        pass
    else:
        return INVALID_CODE()

    uid = test_user_id(username)

    access_token = login_gobelieve(uid, "", config.APP_ID, config.APP_SECRET)
        
    if not access_token:
        return CAN_NOT_GET_TOKEN()

    u0 = user.get_user(rds, uid)
    u = user.User()
    u.uid = uid
    user.save_user(rds, u)

    tok = create_token(3600, True)
    tok['uid'] = uid
    tok['access_token'] = access_token

    t = token.AccessToken(**tok)
    t.save(rds)
    t = token.RefreshToken(**tok)
    t.save(rds)

    return make_response(200, tok)


@app.route("/auth/refresh_token", methods=["POST"])
def refresh_token():
    if not request.data:
        return INVALID_PARAM()

    obj = json.loads(request.data)
    refresh_token = obj["refresh_token"]
    rt = token.RefreshToken()
    if not rt.load(rds, refresh_token):
        return INVALID_REFRESH_TOKEN()

    access_token = login_gobelieve(int(rt.user_id), "", config.APP_ID, config.APP_SECRET)
        
    if not access_token:
        return CAN_NOT_GET_TOKEN()

    tok = create_token(3600, False)
    tok["refresh_token"] = obj["refresh_token"]
    tok["access_token"] = access_token
    tok['uid'] = rt.user_id

    t = token.AccessToken(**tok)
    t.user_id = rt.user_id
    t.save(rds)
    
    return make_response(200, tok)

