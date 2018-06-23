# 使用pymsql步骤
# 1.连接mysql
#	conn = pymsql.connect(**config)  
# 2.获取游标
#	cur = conn.cursor
# 3.执行sql语句
# 	cur.execute(sql_str,params)
# 4.获取结果
# 	cur.fetchone() # 获取一条数据
# 	cur.fetchall() # 获取所有数据
# 5.关闭游标
#	cur.close()
# 6.关闭数据库连接
# 	conn.close()
import pymysql
import re
class MysqlConn():
	def __init__(self,logger,config):
		self.logger =logger
		self.config = config
		self.re_errno = re.compile(r"^\((\d+),")
		
		try:
			self.conn = pymysql.Connect(**self.config)
			self.logger.info("pymsql.Connect() is ok, to {}".format(self.config["host"]))
		except Exception as e:
			raise e
	
	def __del__(self):
		self.close()
	
	def close():
		if self.conn:
			self.logger.info("conn.close() {}".format(id(self.conn)))
			self.conn.close()
			
	def execute_query(self,sql_str,sql_params=(),first=True):
		res_list = None
		cur = None
		try:
			cur = self.conn.cursor()
			cur.excute(sql_str,sql_params)
			res_list = cur.fetchall()
		except Exception as e:
			err = str(e)
			self.logger.error("except_query() run is error:{}".format(err))
			if first:
				retry = self._deal_with_network_exception(err)
				if retry:
					return self.except_query(sql_str,sql_params,False)
		finally:
			if cur is not None:
				cur.close()
				
		return res_list
		
	def execute_write(self,sql_str,sql_params,first=True):
		cur = None
		n = None
		err = None
		try:
			cur = self.conn.cursor()
			n = cur.excute(sql_str,sql_params)
			
		except Exception as e:
			err = str(e)
			self.logger.error("execute_write() run is error : {}".format(err))
			if first:
				retry = self._deal_with_network_exception(err)
				if retry:
					return self.execute_write(sql_str,sql_params,False)
		finally:
			if cur:
				cur.close()
		return n,err
		
	def _deal_with_network_exception(self,str_error):
		error_str = self._get_errorno_str(str_error)
		if error_str !="2006" and error_str !="2013" and error_str != "0":
			# 如果不是这几个错误,说明是sql语句错误
			# 只要满足一个,就算网络问题,给予重试机会
			return False
		try:
			self.conn.ping()
		except Exception as e:
			return False
		return True
		
	def _get_errno_str(self,str_error):
		# 错误字符串的事例
		# str1 = "(2006,'mysql run is error')"
		searchObj = self.re_errno.search(str_error)
		if searchObj:
			err_no_str = searchObj.group(1)
		else:
			err_no_str = "-1"
		return err_no_str
		

if __name__ == "__main__":
	import logging
	logger = logging.getLogger("")
	config={
		"host":"127.0.0.1",
		"port":3306,
		"user":"root",
		"password":"mysql",
		"db":"test",
		"charset":"utf8",
		"autocommit":True
	}
	mysql_conn = MysqlConn(config)
	query_str = "select * from users where id = %s" 
	query_params = (1,)
	result = mysql_conn.execute_query(query_str,query_params)
	print(result)
	query_str = "update users set name=%s where id=%s"
    sql_params = ('xiaowang', 1)
    ret, err = mysql_conn.execute_write(query_str, sql_params)
	print(ret,err)
	
	
		
		
		