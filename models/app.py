# -*- coding: utf-8 -*-
class App(object):
    @classmethod
    def get_store_id(cls, db, appid):
        sql = "SELECT store_id FROM app WHERE app.id=%s"
        r = db.execute(sql, appid)
        app = r.fetchone()
        return app.get('store_id') if app else 0

