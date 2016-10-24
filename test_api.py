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

URL = "http://dev.api.kefu.gobelieve.io:60001"
#URL = "http://api.kefu.gobelieve.io"

url = URL + "/auth/token"
values = {"username":"100060", "password":"111111"}
#values = {"username":"100061", "password":"111111"}
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


params = {"question":"地球距离火星多远"}
url = URL + "/robot/answer"
r = requests.get(url, params=params, headers = headers)
print r.content

url = URL + "/customers/%s/%s"%(7, 1)
r = requests.get(url, headers=headers)
print r.content

