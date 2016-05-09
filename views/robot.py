# -*- coding: utf-8 -*-
import logging
import sys
import xmlrpclib
import config
from flask import request, Blueprint
from libs.util import make_response
from authorization import require_auth

app = Blueprint('robot', __name__)
rpc = xmlrpclib.ServerProxy(config.RPC)

def INVALID_PARAM():
    e = {"error":"问题为空"}
    logging.warn("问题为空")
    return make_response(400, e)

@app.route('/robot/answer', methods=['GET'])
@require_auth
def ask_question():
    store_id = request.store_id
    query = request.args.get('question', '')
    if not query:
        return INVALID_PARAM()

    logging.debug("store id:%s, query:%s", store_id, query)
    try:
        answers = rpc.ask_question(store_id, query)
        logging.debug("answers:%s", answers)
    except xmlrpclib.ProtocolError as err:
        logging.warning("refresh questions err:%s", err)
        answers = []
    except Exception as err:
        logging.warning("refresh questions err:%s", err)
        answers = []

    return make_response(200, answers)
