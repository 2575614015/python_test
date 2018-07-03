import logging
import string
import threading
import pandas as pd
import random

from pymysqlpool import ConnectionPool

config={
	"pool_name":"test",  #  连接池的名字
	"host":"127.0.0.1",  # 数据库ip
	"port":3306,  # 数据库duankou
	"user":"test", # 登陆数据库的数据库账号
	"password":"mysql", # 账号对应的密码
	"database":"test",  # 测试的数据库名字
	"pool_resize_boundary": 50,  # 连接池的最大可扩展上限
	"enable_auto_resize":False,  # 是否支持自动扩展连接数
	"max_pool_size":10 # 启动的默认连接数
}

logging.basicConfig(format="[%(asctime)s][%(name)s][%(module)s.%(lineno)d][%(levelname)s]%(message)s"
					datefmt="%Y-%m-%d %H:%M:%S",
					level=logging.DEBUG
					)

def connection_pool():
	# return a connection pool instance
	pool = ConnectionPool(**config)
	return pool

def test_pool_cursor(cursor_obj=None):
	cursor_obj = cursor_obj or connection_pool().cursor()
	with cursor_obj as cursor:
		print("Truncate table user")
		cursor.execute("TRUNCATE user")
		
		print("Insert one record")
		result = cursor.execute("insert into user(name,age) ")
		
		


		



