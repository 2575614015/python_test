# -*- coding:utf-8 -*-

# 此文件,专门处理静态文件的访问. 不做模板的渲染, 只是转发文件路径

from flask import Blueprint, current_app, make_response
from flask_wtf.csrf import generate_csrf


html = Blueprint('html', __name__)

# (.*)
# 我们只需要1个路由来搞定静态文件的访问


@html.route('/<re(r".*"):file_name>')
def web_html(file_name):
    '''
    127.0.0.1:5000/     index.html
    127.0.0.1:5000/login.html     login.html
    /favicon.ico    固定访问的名字, 我们还需要处理浏览器发出的访问网站小图标的请求
    '''

    # 1. 处理没有文件名, 自行拼接首页
    if not file_name:
        file_name = 'index.html'

    # 2. 如果发现文件名不叫"favicon.ico", 再拼接html/路径
    # favicon.ico: 浏览器为了显示图标, 会自动向地址发出一个请求
    # favicon.ico: 会有缓存,打开浏览器第一次访问该网址时会发出请求.然后缓存起来
    if file_name != 'favicon.ico':
        file_name = 'html/' + file_name

    # 将html当做静态文件返回
    # 3. 如果文件名是'favicon.ico', 就直接返回
    print file_name

    # 创建response
    response = make_response(current_app.send_static_file(file_name))

    # 这里还需要设置csrf_token
    csrf_token = generate_csrf()

    # 设置cookie

    response.set_cookie('csrf_token', csrf_token)
    # Flask-WTF的generate_csrf, 会将cookie中的csrf_token信息, 会同步到session中
    # Flask-Session又会讲session中的csrf_token, 同步到redis中
    # generate_csrf不会每次调用都生成. 会先判断浏览器的cookie中的session里是否有csrf_token信息.没有才重新生成
    # 常规的CSRF保护机制, 是从浏览器的cookie中获取. 而Flask-WTF的扩展机制不一样, 是从session信息中获取csrf_token保护机制

    return response



# @html.route('/')
# def web_html():
#     # 发送静态资源, 而不是渲染模板
#
#     # send_static_file: 会自动指向static文件
#     return current_app.send_static_file('html/index.html')
#
#
# @html.route('/<file_name>')
# def web_html_demo(file_name):
#     # 发送静态资源, 而不是渲染模板
#
#     # send_static_file: 会自动指向static文件
#     return current_app.send_static_file('html/' + file_name)