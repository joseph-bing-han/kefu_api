# -*- coding: utf-8 -*-
from flask import request
from flask import Flask
import flask
import md5
import json
import logging
import sys
import os
import redis

import auth
import config
import authorization



app = Flask(__name__)
app.debug = True

rds = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB)
auth.rds = rds
authorization.rds = rds

app.register_blueprint(auth.app)


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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000)
