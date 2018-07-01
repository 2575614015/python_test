from datetime import datetime
import os
import pymysql
from flask import Flask, render_template, redirect, request, flash, Response, url_for, send_from_directory
import DBUtils
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from flask_wtf.csrf import CSRFProtect
import redis
# from flask_session import Session
from apps.app1 import app1
from pymysql.cursors import DictCursor
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(pathname)s-%(lineno)d %(message)s')  # 配置语句
logger_root = logging.getLogger('')


from utils.re_converters import RegexConverter

app = Flask(__name__)
app.debug=True
app.config["host"]="127.0.0.1"
app.config["port"]=5000
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://test:mysql@192.168.0.107:3306/test"
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["ENABLED"] = True
app.config["SECRET_KEY"] ="12121212"



# CSRFProtect(app)
db=SQLAlchemy(app)

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command("db",MigrateCommand)

redis_store = redis.StrictRedis(port="", host="")


app.register_blueprint(app1,url_prefix="/app1")
from apps.app2 import app2
app.register_blueprint(app2, url_prefix = "/app2")
# Session(app)
app.url_map.converters['re'] = RegexConverter

class BaseModel(object):
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


class User(BaseModel,db.Model):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}   # 如果表已经被创建过,需要加这个参数提供扩展
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),index=True)
    email = db.Column(db.String(32),unique=True)
    password = db.Column(db.String(32))
    # role_id = db.Column(db.Integer,db.ForeignKey("roles.id"))

    def __repr__(self):
        return "<User:%s %s %s %s >"%(self.name,self.id,self.email,self.password)




@app.route("/")
def index():
    return "welcome"

# @app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

app.add_url_rule('/favicon.ico',view_func=favicon)


config = {
    "host":"192.168.0.107",
    "port":3306,
    "user":"test",
    "passwd":"mysql",
    "database":"test",
    "charset":"utf8",
    "cursorclass":DictCursor
}

def connect_db():
    conn = pymysql.Connect(**config)
    return conn


def init_db_by_sql_file(sql_file_path):
    # os.path.join(app2.root_path,"schema.sql")
    with app.app_context():
        conn = connect_db()
        with app.open_resource(sql_file_path, mode="r") as f:
            sqls = f.read().strip().replace("\n", "").split(";")
            sqls.pop()
            for sql in sqls:
                sql = sql + ";"
                conn.cursor().execute(sql)
        conn.commit()


if __name__ == '__main__':
    manager.run()