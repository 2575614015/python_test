import logging
import string
import threading
import pandas as pd
import random

from pymysqlpool import ConnectionPool

config={
	"pool_name":"test",  #  ���ӳص�����
	"host":"127.0.0.1",  # ���ݿ�ip
	"port":3306,  # ���ݿ�duankou
	"user":"test", # ��½���ݿ�����ݿ��˺�
	"password":"mysql", # �˺Ŷ�Ӧ������
	"database":"test",  # ���Ե����ݿ�����
	"pool_resize_boundary": 50,  # ���ӳص�������չ����
	"enable_auto_resize":False,  # �Ƿ�֧���Զ���չ������
	"max_pool_size":10 # ������Ĭ��������
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
		
		


		



