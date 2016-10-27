# -*- coding: utf-8 -*-
import time


class User(object):
    @staticmethod
    def save_user_device_token(rds, appid, uid, device_token, 
                               ng_device_token, xg_device_token,
                               xm_device_token, hw_device_token,
                               gcm_device_token, jp_device_token):
        now = int(time.time())
        key = "users_%d_%d"%(appid, uid)

        if device_token:
            obj = {
                "apns_device_token":device_token,
                "apns_timestamp":now
            }
            rds.hmset(key, obj)
            
        if ng_device_token:
            obj = {
                "ng_device_token":ng_device_token,
                "ng_timestamp":now
            }
            rds.hmset(key, obj)
            
        if xg_device_token:
            obj = {
                "xg_device_token":xg_device_token,
                "xg_timestamp":now
            }
            rds.hmset(key, obj)
            
        if xm_device_token:
            obj = {
                "xm_device_token":xm_device_token,
                "xm_timestamp":now
            }
            rds.hmset(key, obj)

        if hw_device_token:
            obj = {
                "hw_device_token":hw_device_token,
                "hw_timestamp":now
            }
            rds.hmset(key, obj)
        
        if gcm_device_token:
            obj = {
                "gcm_device_token":gcm_device_token,
                "gcm_timestamp":now
            }
            rds.hmset(key, obj)
            
        if jp_device_token:
            obj = {
                "jp_device_token":jp_device_token,
                "jp_timestamp":now
            }
            rds.hmset(key, obj)

        return True


    #重置(清空)用户已经绑定的devicetoken
    @staticmethod
    def reset_user_device_token(rds, appid, uid, device_token, 
                                ng_device_token, xg_device_token, 
                                xm_device_token, hw_device_token, 
                                gcm_device_token, jp_device_token):
        key = "users_%d_%d"%(appid, uid)
        if device_token:
            t = rds.hget(key, "apns_device_token")
            if device_token != t:
                return False
            rds.hdel(key, "apns_device_token")

        if ng_device_token:
            t = rds.hget(key, "ng_device_token")
            if ng_device_token != t:
                return False
            rds.hdel(key, "ng_device_token")
            
        if xg_device_token:
            t = rds.hget(key, "xg_device_token")
            if xg_device_token != t:
                return False
            rds.hdel(key, "xg_device_token")

        if xm_device_token:
            t = rds.hget(key, "xm_device_token")
            if xm_device_token != t:
                return False
            rds.hdel(key, "xm_device_token")

        if hw_device_token:
            t = rds.hget(key, "hw_device_token")
            if hw_device_token != t:
                return False
            rds.hdel(key, "hw_device_token")

        if gcm_device_token:
            t = rds.hget(key, "gcm_device_token")
            if gcm_device_token != t:
                return False
            rds.hdel(key, "gcm_device_token")
        
        if jp_device_token:
            t = rds.hget(key, "jp_device_token")
            if jp_device_token != t:
                return False
            rds.hdel(key, "jp_device_token")

        return True



    @staticmethod
    def save_user(rds, appid, uid, name, avatar, token):
        key = "users_%d_%d"%(appid, uid)
        obj = {
            "access_token":token,
            "name":name,
            "avatar":avatar
        }
        rds.hmset(key, obj)

    @staticmethod
    def set_user_name(rds, appid, uid, name):
        key = "users_%d_%d"%(appid, uid)
        rds.hset(key, "name", name)

    @staticmethod
    def get_user_name(rds, appid, uid):
        key = "users_%d_%d"%(appid, uid)
        return rds.hget(key, "name")

    #用户禁言设置
    @staticmethod
    def set_user_forbidden(rds, appid, uid, fb):
        key = "users_%d_%d"%(appid, uid)
        rds.hset(key, "forbidden", fb)

    #群组免打扰设置
    @staticmethod
    def get_user_notification_quiet(rds, appid, uid, group_id):
        key = "users_%s_%s"%(appid, uid)
        quiet = rds.hget(key, "group_%d"%group_id)
        q = int(quiet) if quiet else 0
        return q

    @staticmethod
    def set_user_notification_quiet(rds, appid, uid, group_id, quiet):
        key = "users_%s_%s"%(appid, uid)
        q = 1 if quiet else 0
        rds.hset(key, "group_%d"%group_id, q)

    @staticmethod
    def add_user_count(rds, appid, uid):
        key = "statistics_users_%d"%appid
        rds.pfadd(key, uid)

