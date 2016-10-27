import flask
import json
import random

def make_response(status_code, data = None):
    if data:
        res = flask.make_response(json.dumps(data), status_code)
        res.headers['Content-Type'] = "application/json"
    else:
        res = flask.make_response("", status_code)

    return res


def make_json_response(obj, status_code=200):
    if obj:
        res = flask.make_response(json.dumps(obj), status_code)
        res.headers['Content-Type'] = "application/json"
    else:
        res = flask.make_response("", status_code)

    return res



UNICODE_ASCII_CHARACTER_SET = ('abcdefghijklmnopqrstuvwxyz'
                               'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                               '0123456789')

def random_token_generator(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
    rand = random.SystemRandom()
    return ''.join(rand.choice(chars) for x in range(length))

def create_token(expires_in, refresh_token=False):
    """Create a BearerToken, by default without refresh token."""

    token = {
        'access_token': random_token_generator(),
        'expires_in': expires_in,
        'token_type': 'Bearer',
    }
    if refresh_token:
        token['refresh_token'] = random_token_generator()

    return token
