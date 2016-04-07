# -*- coding: utf-8 -*-

import requests
import urllib
import urllib2
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

import threading
import json
import sys

#URL = "http://192.168.33.10"
URL = "http://dev.gobelieve.io:6000"

url = URL + "/auth/token"
values = {"username":"13800000000@gobelieve.io", "password":"11111111"}
data = json.dumps(values)
r = requests.post(url, data=data)
print r.content
resp = json.loads(r.content)
print resp
print "access token:", resp["access_token"]
print "refresh token:", resp["refresh_token"]
access_token = resp["access_token"]
refresh_token = resp["refresh_token"]

url = URL + "/auth/refresh_token"
headers = {}
headers["Authorization"] = "Bearer " + access_token
 
values = {"refresh_token":refresh_token}
data = json.dumps(values)
r = requests.post(url, data=data, headers = headers)
print r.content
resp = json.loads(r.content)
 
print "access token:", resp["access_token"]
print "refresh token:", resp["refresh_token"]
access_token = resp["access_token"]
refresh_token = resp["refresh_token"]
