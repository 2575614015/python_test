# -*- coding:utf-8 -*-

# 公用的工具类

from werkzeug.routing import BaseConverter
from flask import session, g, jsonify
from ihome.utils.response_code import RET
from functools import wraps


class RegexConverter(BaseConverter):
    def __init__(self, url_map, regex):
        super(RegexConverter, self).__init__(url_map)
        self.regex = regex


def login_required(view_func):
    '''检查用户的登录状态'''
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        # 核心逻辑:获取session的id
        user_id = session.get('user_id')
        if user_id is not None:
            # 表示用户已登录
            # 后面的接口, 可能仍然需要user_id数据,来进行数据库的查询
            # 此时,为了方便,可以使用g变量来记录
            g.user_id = user_id
            return view_func(*args, **kwargs)
        else:
            return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')

    return wrapper