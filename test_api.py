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
uid = resp['uid']


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


def TestQuestion():
    params = {"question":"地球距离火星多远"}
    url = URL + "/robot/answer"
    r = requests.get(url, params=params, headers = headers)
    print r.content

def TestCustomerName():
    url = URL + "/customers/%s/%s"%(7, 1)
    r = requests.get(url, headers=headers)
    print r.content
    

def TestUnregister():
    url = URL + "/auth/unregister"
    r = requests.post(url, data="", headers=headers)
    assert(r.status_code == 200)
    print "unregister success:",  r.content

def TestOnlineAndOffline():
    url = URL + "/users/%s"%uid
    data = json.dumps({"status":"online"})
    r = requests.patch(url, data=data, headers=headers)
    assert(r.status_code == 200)
    print "online success:",  r.content


    data = json.dumps({"status":"offline"})
    r = requests.patch(url, data=data, headers=headers)
    assert(r.status_code == 200)
    print "offline success:",  r.content
    

    
def TestPush():
    url = URL + "/push/bind"

    data = {
        #"ng_device_token":"292854919A9A4E4E1818ABABF2F6ADC9",
        "xg_device_token":"adb238518d682b2e49cba26c207f04a712c6da46",
        #"xm_device_token":"d//igwEhgBGCI2TG6lWqlOlzU8pu8+C4t+wQ4zMxFYhLO0pHWInlKmKMyW9I3gWgby1Z1vq59TkIQQYeaS43gEzCfwuNRp+OkuHM3JCDA5U=",
        #"hw_device_token":"08650300127619392000000630000001",
        #"apns_device_token":"177bbe6da89125b84bfad60ff3d729005792fad4ebbbf5729a8cecc79365a218",
        #"gcm_device_token":"fNMMmCwoba0:APA91bGqpKqwMvbxNlAcGj6wILQoCAY59wx3huFculEkUyElnidJvuEgwVVFuD3PKBUoLIop8ivJlXlkJNPYfFAnabHPAn8_o4oeX1b8eIaOQLmVOkXY-sUw-QAY4MF9PG4RL3TDq7e6",
        #"jp_device_token":"111111",
    }
    r = requests.post(url, data=json.dumps(data), headers = headers)
    assert(r.status_code == 200)

    print "bind device token success:", r.content

    url = URL + "/push/unbind"
    r = requests.post(url, data=json.dumps(data), headers = headers)
    assert(r.status_code == 200)

    print "unbind device token success:", r.content


TestUnregister()
TestOnlineAndOffline()
TestPush()
