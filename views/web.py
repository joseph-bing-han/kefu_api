# -*- coding: utf-8 -*-
import requests
from flask import request, Blueprint, g, session, redirect
from flask import render_template_string, render_template
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
import flask
import md5
import json
import base64
import logging
from models.seller import Seller
from models.store import Store
from models.app import App
from libs.util import make_response

from authorization import check_seller_password

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
        return render_template('customer_support/chat.html', host=config.HOST, name=seller['name'],
                               apiURL=config.APIURL)
    else:
        return render_template('customer_support/index.html')


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username:
        return render_template_string(error_html, error="用户名称为空")
    if not password:
        return render_template_string(error_html, error="密码为空")

    password_md5 = md5.new(password).hexdigest()
    db = g._db

    uid = None
    store_id = None
    seller = Seller.get_seller_with_number(db, username)

    if check_seller_password(seller, password):
        uid = seller['id']
        store_id = seller['store_id']
    else:
        try:
            seller_id = int(username)
            seller = Seller.get_seller(db, seller_id)
            if check_seller_password(seller, password):
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
    username = request.args.get('name', '')
    device_id = request.args.get('device_id', '')
    if not store and appid:
        store = App.get_store_id(g._db, int(appid))
        print "store id:", store
        if not store:
            return render_template_string(error_html, error="非法的应用id")
        
    if not store:
        return render_template_string(error_html, error="未指定商店id")
        
    s = Store.get_store(g._db, int(store))
    if s:
        name = s['name']
    else:
        name = ""

    if uid and appid and token:
        return render_template("customer/chat.html",
                               host=config.HOST,
                               customerAppID=int(appid),
                               customerID=int(uid),
                               customerToken=token,
                               name=name,
                               apiURL=config.APIURL,
                               storeID=int(store))

    # 生成临时用户
    rds = g.rds
    key = "anonymous_id"
    uid = rds.incr(key)
    appid = config.ANONYMOUS_APP_ID
    token = login_gobelieve(uid, username,
                            config.ANONYMOUS_APP_ID,
                            config.ANONYMOUS_APP_SECRET,
                            device_id=device_id)
    return render_template("customer/chat.html",
                           host=config.HOST,
                           customerAppID=appid,
                           customerID=uid,
                           customerToken=token,
                           name=name,
                           apiURL=config.APIURL,
                           storeID=int(store))


@app.route("/chat/index.html")
def chat_page():
    appid = request.args.get('appid')
    appkey = request.args.get('appkey')
    customer_id = request.args.get('customer_id', '')
    app_name = request.args.get('app_name', '')
    user_name = request.args.get('name', '')
    if not appid or not appkey or not user_name:
        return render_template_string(error_html, error="appid、appkey、uid、user_name 为必填参数")

    data = {
        "appid": int(appid),
        "customer_id": customer_id,
        "name": user_name,
    }

    basic = base64.b64encode("%s:%s" % (appid, appkey))
    headers = {'Content-Type': 'application/json; charset=UTF-8',
               'Authorization': 'Basic ' + basic}
    url = config.GOBELIEVE_URL + "/customer/register"
    r = requests.post(url, headers=headers, data=json.dumps(data))
    if r.status_code != 200:
        return render_template_string(error_html, error="获取权限失败")

    res = json.loads(r.content)
    client_id = res['data']['client_id']
    store_id = res['data']['store_id']
    token = res['data']['token']
    print res['data']

    return render_template("customer/chat.html", host=config.HOST,
                           customerAppID=int(appid), customerID=int(client_id),
                           customerToken=token, store_id=store_id,
                           name=app_name, apiURL=config.APIURL)


@app.route("/upload", methods=['POST'])
def upload():
    url = 'http://api.gobelieve.io/images'
    # url = 'http://0.0.0.0:8001/images/upload'
    data = request.form.get('data', '')
    content_type = request.form.get('contentType', '')
    authorization = request.form.get('authorization', '')
    headers = {'Authorization': authorization, 'Content-Type': content_type}
    response = requests.post(url, base64.b64decode(data), headers=headers)
    print response.content
    return make_response(200, json.loads(response.content))


@app.route("/chat/pc/conversation.html")
def chat_conversation():
    uid = request.args.get('uid')
    appid = request.args.get('appid')
    token = request.args.get('token')

    if uid and appid and token:
        return render_template("customer/conversation.html", host=config.HOST, apiURL=config.APIURL)
    else:
        return "没有用户信息"


@app.route("/stores/<int:store_id>")
def get_store(store_id):
    s = Store.get_store(g._db, store_id)
    obj = {
        "store_id": store_id,
        "name": ''
    }

    if s:
        obj['name'] = s['name']

    return make_response(200, obj)
