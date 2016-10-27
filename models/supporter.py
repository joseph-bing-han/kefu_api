# -*- coding: utf-8 -*-
import time


class Supporter(object):

    @staticmethod
    def set_user_online(rds, uid):
        key = "supporters_%d"%uid
        rds.hset(key, "status", "online")

    @staticmethod
    def set_user_offline(rds, uid):
        key = "supporters_%d"%uid
        rds.hset(key, "status", "offline")
