# -*- coding: utf-8 -*-
import logging
import sys
import xmlrpclib
import config
from flask import request, Blueprint
from util import make_response

app = Blueprint('robot', __name__)
s = xmlrpclib.ServerProxy('http://localhost:8000')

@app.route('/robot/answer', methods=['GET'])
def ask_question():
    query = request.args.get('question', '')
    if not query:
        return ""
    logging.debug("query:%s", query)
    answers = s.ask_question(query)

    return make_response(200, answers)
