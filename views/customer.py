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
        return rds.hget(key, "name")

@app.route("/customers/<int:appid>/<int:customer_id>")
@require_auth
def get_customer(appid, customer_id):
    rds = g.imrds
    name = Customer.get_customer_name(rds, appid, customer_id)
    if not name:
        name = ""
    obj = {
        "appid":appid,
        "uid":customer_id,
        "name":name
    }

    return make_response(200, obj)
