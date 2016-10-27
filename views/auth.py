# -*- coding: utf-8 -*-
from flask import request, Blueprint, g, session, render_template_string
import random
import json
import time
import requests
import urllib
import logging
import base64
import md5
from datetime import datetime
from functools import wraps

from werkzeug.security import generate_password_hash, check_password_hash

from authorization import require_auth
from authorization import check_seller_password
from libs.util import make_json_response
from libs.util import create_token
from gobelieve import login_gobelieve
from gobelieve import send_sys_message
from models import token
from models.seller import Seller
from models.supporter import Supporter
from models.user import User

import config

app = Blueprint('auth', __name__)

def INVALID_PARAM():
    e = {"error":"非法输入"}
    logging.warn("非法输入")
    return make_json_response(e, 400)


def INVALID_USER():
    e = {"error":"非法的用户名或密码"}
    logging.warn("非法的用户名或密码")
    return make_json_response(e, 400)
    
def INVALID_REFRESH_TOKEN():
    e = {"error":"非法的refresh token"}
    logging.warn("非法的refresh token")
    return make_json_response(e, 400)
    
def CAN_NOT_GET_TOKEN():
    e = {"error":"获取imsdk token失败"}
    logging.warn("获取imsdk token失败")
    return make_json_response(e, 400)


    
@app.route("/auth/unregister", methods=["POST"])
@require_auth
def unregister():
    uid = request.uid
    store_id = request.store_id

    obj = {}
    if request.data:
        obj = json.loads(request.data)

    device_token = obj["apns_device_token"] if obj.has_key("apns_device_token") else ""
    ng_device_token = obj["ng_device_token"] if obj.has_key("ng_device_token") else ""
    xg_device_token = obj["xg_device_token"] if obj.has_key("xg_device_token") else ""
    xm_device_token = obj["xm_device_token"] if obj.has_key("xm_device_token") else ""
    hw_device_token = obj["hw_device_token"] if obj.has_key("hw_device_token") else ""
    gcm_device_token = obj["gcm_device_token"] if obj.has_key("gcm_device_token") else ""
    jp_device_token = obj["jp_device_token"] if obj.has_key("jp_device_token") else ""
    
    User.reset_user_device_token(g.imrds, config.APP_ID, uid, device_token, ng_device_token, 
                                 xg_device_token, xm_device_token, hw_device_token,
                                 gcm_device_token, jp_device_token)

    Supporter.set_user_offline(g.imrds, uid)

    return make_json_response({"success":True}, 200)
    
@app.route("/auth/token", methods=["POST"])
def access_token():
    if not request.data:
        return INVALID_PARAM()

    obj = json.loads(request.data)
    username = obj["username"]
    password = obj["password"]

    platform = obj.get('platform')
    device_id = obj.get('device_id', '')

    if not username or not password:
        return INVALID_PARAM()

    db = g._db
    rds = g.rds

    uid = None
    store_id = None

    try:
        seller_id = int(username)
    except ValueError:
        seller_id = 0

    if seller_id:
        seller = Seller.get_seller(db, seller_id)
    else:
        seller = Seller.get_seller_with_number(db, username)

    if check_seller_password(seller, password):
        uid = seller['id']
        store_id = seller['store_id']

    if not uid:
        return INVALID_USER()

    access_token = login_gobelieve(uid, seller['name'], 
                                   config.APP_ID, config.APP_SECRET, 
                                   device_id, platform)
        
    if not access_token:
        return CAN_NOT_GET_TOKEN()

    tok = create_token(3600, True)
    tok['uid'] = uid
    tok['store_id'] = store_id
    tok['access_token'] = access_token
    tok['name'] = seller['name']
    tok['status'] = 'online'

    t = token.AccessToken(**tok)
    t.save(rds)
    t = token.RefreshToken(**tok)
    t.save(rds)

    #用户上线
    Supporter.set_user_online(rds, uid)

    now = int(time.time())
    obj = {
        "timestamp":now,
        "device_name":obj.get("device_name", ""),
        "device_id":obj.get("device_id", ""),
        "platform":obj.get("platform", 0)
    }

    content = json.dumps({"login":obj})
    send_sys_message(uid, content, config.APP_ID, config.APP_SECRET)

    return make_json_response(tok, 200)


@app.route("/auth/refresh_token", methods=["POST"])
def refresh_token():
    if not request.data:
        return INVALID_PARAM()

    db = g._db
    obj = json.loads(request.data)
    refresh_token = obj["refresh_token"]
    rt = token.RefreshToken()
    if not rt.load(g.rds, refresh_token):
        return INVALID_REFRESH_TOKEN()

    access_token = login_gobelieve(int(rt.user_id), "", config.APP_ID, config.APP_SECRET)
        
    if not access_token:
        return CAN_NOT_GET_TOKEN()

    seller = Seller.get_seller(db, rt.user_id)
    tok = create_token(3600, False)
    tok["refresh_token"] = obj["refresh_token"]
    tok["access_token"] = access_token
    tok['uid'] = rt.user_id
    tok['store_id'] = seller['store_id']
    tok['name'] = seller['name']

    t = token.AccessToken(**tok)
    t.user_id = rt.user_id
    t.save(g.rds)
    
    return make_json_response(tok, 200)


