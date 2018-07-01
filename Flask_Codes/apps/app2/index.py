from . import app2
import os
import pymysql
from pymysql.cursors import DictCursor
from flask import Flask,request,session,g,redirect,url_for
from flask import abort,render_template,flash



config = {
    "HOST":"192.168.0.107",
    "PORT":3306,
    "USER":"test",
    "PASSWORD":"mysql",
    "DATABASE":"test",
    "CHARSET":"utf8",
    "CURSOR":DictCursor
}


def connect_db():
    conn = pymysql.Connect(**config)
    return conn


def init_db():
    with app2.app_context_processor():
        conn = connect_db()
        with app2.open_resource(os.path.join(app2.root_path,"schema.sql"), mode="r") as f:
            conn.cousor().executescript(f.read())
        conn.commit()



if __name__ == '__main__':
    app2.run()