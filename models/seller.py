# -*- coding: utf-8 -*-

class Seller(object):
    @classmethod
    def get_seller(cls, db, seller_id):
        sql = "SELECT id, name, password, store_id FROM seller WHERE id=%s"
        r = db.execute(sql, seller_id)
        return r.fetchone()

    @classmethod
    def get_seller_with_number(cls, db, number):
        sql = "SELECT id, name, password, store_id FROM seller WHERE number=%s"
        r = db.execute(sql, number)
        return r.fetchone()
