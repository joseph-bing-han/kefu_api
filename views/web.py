# -*- coding: utf-8 -*-
from flask import request, Blueprint, g, session, redirect
from flask import render_template_string, render_template
import md5
import flask
from models.seller import Seller

from gobelieve import login_gobelieve
import config

app = Blueprint('web', __name__)

error_html = """<!DOCTYPE html>
<html>
<head>
<title>Chat Demo</title>
</head>
<body>


<p>error.</p>

</body>
</html>"""


@app.route('/')
def index():
    if request.cookies.get('token'):
        return render_template('chat.html', host=config.HOST)
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

    access_token = login_gobelieve(uid, "", config.APP_ID, config.APP_SECRET)
        
    if not access_token:
        return render_template_string(error_html, error="登录失败")

    response = flask.make_response(redirect('/'))

    response.set_cookie('token', access_token)
    response.set_cookie('name', seller['name'])
    response.set_cookie('store_id', str(seller['store_id']))
    response.set_cookie('uid', str(seller['id']))
    return response

