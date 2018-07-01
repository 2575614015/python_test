# _*_ coding: utf-8 _*_

__author__ = "xiaohe"

import pymysql
import re

class MysqlConn():
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.re_errno = re.compile(r'^\((\d+),')

        try:
            self.conn = pymysql.Connect(**self.config)
            self.logger.info("pymysql.Connect() ok, {0}".format(id(self.conn)))
        except Exception as e:
            raise e

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



if __name__ == "__main__":
    """
    TODO: 1. autocomit为false的时候, 在失败的时候  rollback
          2. query: execute_query 增加支持游标操作 for row in cur:
    """
    import logging
    logger = logging.getLogger('')
    config = {
        "host": "192.168.0.107",
        "port": 3306,
        "user": "test",
        "password": "mysql",
        "db": "test",
        "autocommit": True,
        # "cursorclass": pymysql.cursors.DictCursor,
        "charset": "utf8"
    }

    mysql_conn = MysqlConn(logger, config)
    # query_str = "insert into test1 set id=%s, title=%s, author=%s"
    # sql_params = (2, 'titlessssssss', 'author中文啊1111111')
    # n = mysql_conn.execute_write(query_str, sql_params)
    # print(n)

    #  mysql NULL 对应 python None

    mysql_conn.close()
    query_str = "select * from test1 where id=%s"
    sql_params = (3)
    resul_list = mysql_conn.execute_query(query_str, sql_params)
    # resul_list = mysql_conn.execute_query(query_str, sql_params)
    print(resul_list)

    # tb = {
    #     "a": '|近十年来，全国经济高速发展，全国个',
    #     "b": 1
    # }
    # import json
    # query_str = "update test1 set title=%s, author=%s where id=%s"
    # sql_params = ('|深圳前海中高基金管理有限公司', json.dumps(tb, ensure_ascii=False), 2)
    # resul_list = mysql_conn.execute_write(query_str, sql_params)
    # print(resul_list)

    # query_str = "update test1 set oid=%s where id=%s"
    # sql_params = ('333333333333333', 2)
    # ret, err = mysql_conn.execute_write(query_str, sql_params)
    # print(ret, err)
    # if "(1062," in err:
    #     print("find")