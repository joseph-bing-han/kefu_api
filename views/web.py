# -*- coding: utf-8 -*-
from flask import request, Blueprint, g, session, redirect
from flask import render_template_string, render_template
import flask
import md5
import json
import base64
import logging
from models.seller import Seller
from models.store import Store

from gobelieve import login_gobelieve
import config

app = Blueprint('web', __name__)

error_html = """<!DOCTYPE html>
<html>
<head>
<title>客服</title>
</head>
<body>


<p>{{error}}</p>

</body>
</html>"""


@app.route('/')
def index():
    if request.cookies.get('token') and request.cookies.get('uid'):
        uid = request.cookies.get('uid')
        uid = int(uid)
        seller = Seller.get_seller(g._db, uid)
        return render_template('chat.html', host=config.HOST, name=seller['name'])
    else:
        return render_template('index.html')


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username:
        return render_template_string(error_html, error="用户名称为空")
    if not password:
        return render_template_string(error_html, error="密码为空")
    
    
    password = md5.new(password).hexdigest()
    db = g._db

    uid = None
    store_id = None
    seller = Seller.get_seller_with_number(db, username)
    if seller and seller['password'] == password:
        uid = seller['id']
        store_id = seller['store_id']
    else:
        try:
            seller_id = int(username)
            seller = Seller.get_seller(db, seller_id)
            if seller and seller['password'] == password:
                uid = seller['id']
                store_id = seller['store_id']
        except ValueError:
            pass
            
    if not uid:
        return render_template_string(error_html, error="非法的用户名/密码")

    name = seller.get('name')
    if not name:
        name = ""
    access_token = login_gobelieve(uid, name, config.APP_ID, config.APP_SECRET)
        
    if not access_token:
        return render_template_string(error_html, error="登录失败")

    response = flask.make_response(redirect('/'))

    response.set_cookie('token', access_token)
    response.set_cookie('store_id', str(seller['store_id']))
    response.set_cookie('uid', str(seller['id']))
    return response

@app.route("/chat/pc/index.html")
def chat():
    store = request.args.get('store')
    uid = request.args.get('uid')
    appid = request.args.get('appid')
    token = request.args.get('token')

    if not store:
        return render_template_string(error_html, error="未指定商店id")
    
    s = Store.get_store(g._db, int(store))
    if s:
        name = s['name']
    else:
        name = ""
    
    if uid and appid and token:
        return render_template("customer_chat.html", host=config.HOST, customerAppID=int(appid), customerID=int(uid), customerToken=token, name=name)

    #生成临时用户
    rds = g.rds
    key = "anonymous_id"
    uid = rds.incr(key)
    appid = config.ANONYMOUS_APP_ID
    token = login_gobelieve(uid, "", config.ANONYMOUS_APP_ID, config.ANONYMOUS_APP_SECRET)
    return render_template("customer_chat.html", host=config.HOST, customerAppID=appid, customerID=uid, customerToken=token, name=name)
