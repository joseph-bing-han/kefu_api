# -*- coding: utf-8 -*-
from flask import request
from flask import Flask
from flask import g
import flask
import md5
import json
import logging
import sys
import os
import redis

from views import auth
from libs.mysql import Mysql
from libs.util import make_response
import config

app = Flask(__name__)
app.debug = config.DEBUG

rds = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB)

def SERVER_INTERNAL_ERROR():
    e = {"error":"Server Internal Error!"}
    logging.error("server internal error")
    return make_response(500, e)


def generic_error_handler(err):
    logging.exception(err)
    return SERVER_INTERNAL_ERROR()

def before_request():
    logging.debug("before request")
    g.rds = rds

    cnf = config.MYSQL
    g._db = Mysql(*cnf)

def app_teardown(exception):
    logging.debug('app_teardown')
    # 捕获teardown时的mysql异常
    try:
        db = getattr(g, '_db', None)
        if db:
            db.close()

    except Exception:
        pass


def init_app(app):
    app.teardown_appcontext(app_teardown)
    app.before_request(before_request)
    app.register_error_handler(Exception, generic_error_handler)

    app.register_blueprint(auth.app)
    if config.ENABLE_ROBOT:
        from views import robot
        app.register_blueprint(robot.app)


def init_logger(logger):
    root = logger
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(filename)s:%(lineno)d -  %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)    

log = logging.getLogger('')
init_logger(log)

init_app(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=60001)
