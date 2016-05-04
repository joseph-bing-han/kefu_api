# -*- coding: utf-8 -*-

from flask import request, g
from functools import wraps
import logging
import random
import time
import web
import json
import base64
import md5
import requests

from models import token
from libs.util import make_response
import config

def INVALID_ACCESS_TOKEN():
    e = {"error":"非法的access token"}
    logging.warn("非法的access token")
    return make_response(400, e)
def EXPIRE_ACCESS_TOKEN():
    e = {"error":"过期的access token"}
    logging.warn("过期的access token")
    return make_response(400, e)

def require_auth(f):
    """Protect resource with specified scopes."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.cookies.get('token'):
            s = request.cookies.get('store_id', '')
            u = request.cookies.get('uid', '')
            if s and u:
                request.uid = int(u)
                request.store_id = int(s)
            return f(*args, **kwargs)

        if 'Authorization' in request.headers:
            tok = request.headers.get('Authorization')[7:]
        else:
            return INVALID_ACCESS_TOKEN()
        t = token.AccessToken()
        if not t.load(g.rds, tok):
            return INVALID_ACCESS_TOKEN()
        if time.time() > t.expires:
            print t.expires, time.time()
            return EXPIRE_ACCESS_TOKEN()
        request.uid = int(t.user_id)
        request.store_id = int(t.store_id)
        return f(*args, **kwargs)
    return wrapper
    



