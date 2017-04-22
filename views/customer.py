# -*- coding: utf-8 -*-
from flask import request, Blueprint, g
import json
import logging
from libs.util import make_response
from authorization import require_auth

app = Blueprint('customer', __name__)

class Customer(object):
    @staticmethod
    def get_customer_name(rds, appid, uid):
        key = "users_%d_%d"%(appid, uid)
        return rds.hmget(key, "name", "avatar")
    
class App(object):
    @classmethod
    def get_app(cls, db, appid):
        sql = "SELECT app.id as id, app.name as name, client.id as client_id, client.platform_type as platform_type FROM app, client WHERE app.id=%s AND app.id=client.app_id"
        r = db.execute(sql, appid)

        PLATFORM_WECHAT = 3
        app = {"wechat":False}
        for o in r.fetchall():
            app['id'] = o['id']
            app['name'] = o['name']
            if o['platform_type'] == PLATFORM_WECHAT:
                app['wechat'] = True
                
        return app if app.get('id') else None
    
@app.route("/customers/<int:appid>/<int:customer_id>")
@require_auth
def get_customer(appid, customer_id):
    rds = g.imrds
    name, avatar = Customer.get_customer_name(rds, appid, customer_id)
    if not name:
        name = ""
    if not avatar:
        avatar = ""

    obj = {
        "appid":appid,
        "uid":customer_id,
        "name":name,
        "avatar":avatar
    }

    return make_response(200, obj)


@app.route("/customers/<int:appid>")
@require_auth
def get_customer_app(appid):
    app = App.get_app(g._db, appid)
    if app:
        obj = {
            "id":appid,
            "name":app['name'],
            "wechat":app['wechat']
        }
        return make_response(200, obj)
    else:
        return make_response(404, {"error":"not found"})
