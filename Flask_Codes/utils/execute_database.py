from pymysql.cursors import DictCursor
from flask_code_1 import  app,logger_root
import os
import pymysql
import re

class Database_Execute(object):
    __conn = None
    config = {
        "host": "192.168.0.107",
        "port": 3306,
        "user": "test",
        "passwd": "mysql",
        "database": "test",
        "charset": "utf8",
        "cursorclass": DictCursor
    }
    def __init__(self):
        self.conn = pymysql.Connect(**Database_Execute.config)
        self.logger = logger_root
        self.re_errno = re.compile(r'^\((\d+),')

    def init_db_by_sql_file(self, sql_file_path):
        # os.path.join(app2.root_path,"schema.sql")
        with app.app_context():
            conn = self.conn()
            with app.open_resource(sql_file_path, mode="r") as f:
                sqls = f.read().strip().replace("\n", "").split(";")
                sqls.pop()
                for sql in sqls:
                    sql = sql + ";"
                    try:
                        conn.cursor().execute(sql)
                    except Exception as e:
                        self.logger.error(e)
            conn.commit()

    def __del__(self):
        self.close()

    def close(self):
        if self.conn:
            self.logger.info("conn.close() {0}".format(id(self.conn)))
            self.conn.close()

    def execute_query(self, sql_str, sql_params=(), first=True):
        res_list = None
        cur = None
        try:
            cur = self.conn.cursor()
            cur.execute(sql_str, sql_params)
            res_list = cur.fetchall()
        except Exception as e:
            err = str(e)
            self.logger.error('execute_query: {0}'.format(err))
            if first:
                retry = self._deal_with_network_exception(err)
                if retry:
                    # self.logger.error('retry "{0}"'.format(sql_str))
                    return self.execute_query(sql_str, sql_params, False)
        finally:
            if cur is not None:
                cur.close()
        return res_list

    def execute_write(self, sql_str, sql_params=(), first=True):
        cur = None
        n = None
        err = None
        try:
            cur = self.conn.cursor()
            n = cur.execute(sql_str, sql_params)
            # self.logger.info("{0}".format(cur.mogrify(sql_str, sql_params)))
        except Exception as e:
            err = str(e)
            self.logger.error('execute_query: {0}'.format(err))
            if first:
                retry = self._deal_with_network_exception(err)
                if retry:
                    return self.execute_write(sql_str, sql_params, False)
        finally:
            if cur is not None:
                cur.close()
        return n, err

    def _deal_with_network_exception(self, stre):
        errno_str = self._get_errorno_str(stre)
        if errno_str != '2006' and errno_str != '2013' and errno_str != '0':
            return False
        try:
            self.conn.ping()
        except Exception as e:
            return False
        return True

    def _get_errorno_str(self, stre):
        # https://www.cnblogs.com/skillCoding/archive/2011/09/07/2169932.html
        # str1 = '(2006, "MySQL server has gone away (BrokenPipeError(32, \'Broken pipe\'))")'
        searchObj = self.re_errno.search(stre)
        if searchObj:
            errno_str = searchObj.group(1)
        else:
            errno_str = '-1'
        return errno_str


