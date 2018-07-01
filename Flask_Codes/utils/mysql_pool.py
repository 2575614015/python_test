import pymysql
from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB

config = {
    "DBHOST":"192.168.0.107",
    "DBPORT":3306,
    "DBUSER":"root",
    "DBPASSWORD":"mysql",
    "DBCHAR":"utf8",
    "DBNAME":"test"
}

class MysqlPool(object):
    __pool = False
    __init = False
    def __init__(self):
        if not MysqlPool.__init:
            self._conn = PooledDB(creator=pymysql, mincached=1, maxcached=20, host=config["HOST"],
                         port=config["DBPORT"], db=config["DBNAME"], user=config["DBUSER"],
                         passworld=config["DBPASSWORD"], charset=config["DBCHAR"],
                         use_unicode=False, cursorclass=DictCursor, autocommit=True
                         ).connection()

    def __new__(cls, *args, **kwargs):
        if not cls.__pool:
            cls.__pool = object.__new__(cls)
        return cls.__pool

    def __del__(self):
        if self._conn:
            self._conn.close()

    def __repr__(self):
        return "连接池的id是 %s" % id(self._conn)
    # @staticmethod
    # def __get_conn():
    #     if MysqlPool.__pool is None:
    #         MysqlPool.__pool = PooledDB(creator=pymysql,mincached=1,maxcached=20,host=config["HOST"],
    #                                     port=config["DBPORT"],db=config["DBNAME"],user=config["DBUSER"],
    #                                     passworld=config["DBPASSWORD"],charset=config["DBCHAR"],
    #                                     use_unicode=False,cursorclass=DictCursor,autocommit=True
    #                                     )
    #     return MysqlPool.__pool.connection()

    def get_all(self,sql,params=()):
        result = None
        with self._conn.cursor() as cursor:
            count = cursor.execute(sql,params)
            if count > 0:
                result = cursor.fetchallDict()
        return result

    def get_one(self,sql,params=()):
        result = None
        with self._conn.cursor() as cursor:
            count = cursor.execute(sql, params)
            if count > 0:
                result = cursor.fetchoneDict()
        return result

    def get_many(self,sql,params=()):
        result = None
        with self._conn.cursor() as cursor:
            count = cursor.execute(sql, params)
            if count > 0:
                result = cursor.fetchmanyDict()
        return result

    def insert_delete_update(self,sql,params=()):
        with self._conn.cursor() as cursor:
            count = cursor.execute(sql, params)
        return count




