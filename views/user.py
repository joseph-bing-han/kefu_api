# -*- coding: utf-8 -*-

from flask import request, Blueprint, g
import logging
import json
from libs.util import make_json_response
from authorization import require_auth
from models import Supporter

app = Blueprint('user', __name__)

#用户上线/下线
@app.route("/users/<int:uid>", methods=["PATCH"])
@require_auth
def update_user(uid):
    obj = json.loads(request.data)
    if obj.has_key('status'):
        if obj['status'] == 'online':
            Supporter.set_user_online(g.imrds, uid)
        elif obj['status'] == 'offline':
            Supporter.set_user_offline(g.imrds, uid)
        else:
            raise ResponseMeta(400, 'invalid status')

    return make_json_response({"success":True}, 200)


