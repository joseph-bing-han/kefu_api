
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

@app.route('/messages', methods=['GET'])
@require_auth
def get_messages():
    appid = config.APP_ID
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
        response = flask.make_response(json.dumps(obj.get("data")), 200)
    else:
        response = flask.make_response(resp.content, resp.status_code)
    response.headers['Content-Type'] = "application/json"
    return response
