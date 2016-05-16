
# -*- coding: utf-8 -*-
import config
import requests
from urllib import urlencode
from flask import request, Blueprint
import flask
import logging
import json
import config
from authorization import require_auth

app = Blueprint('message', __name__)

im_url=config.IM_RPC_URL


MSG_CUSTOMER = 24;
MSG_CUSTOMER_SUPPORT = 25;


def is_in_store(m, store_id):
    if m['command'] == MSG_CUSTOMER or \
       m['command'] == MSG_CUSTOMER_SUPPORT:
        if m['store_id'] == store_id:
            return True

    return False


@app.route('/messages', methods=['GET'])
@require_auth
def get_messages():
    appid = request.args.get('appid')
    if appid:
        appid = int(appid)
    else:
        appid = config.APP_ID

    store_id = request.args.get('store_id')
    if store_id:
        store_id = int(store_id)

    uid = request.args.get('uid')
    if uid:
        uid = int(uid)
    else:
        uid = request.uid

    limit = int(request.args.get('limit', '500'))
    if limit > 1000:
        limit = 1000

    params = {
        "appid": appid,
        "uid": uid,
        "limit":limit
    }
    
    logging.debug("limit:%s", limit)
    url = im_url + "/load_latest_message"
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        obj = json.loads(resp.content)
        msgs = obj.get("data")
        #过滤出此商店的消息
        if store_id:
            msgs = [m for m in msgs if is_in_store(m, store_id)]

        response = flask.make_response(json.dumps(msgs), 200)
    else:
        response = flask.make_response(resp.content, resp.status_code)
    response.headers['Content-Type'] = "application/json"
    return response
