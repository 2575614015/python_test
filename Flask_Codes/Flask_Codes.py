from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand

app = Flask(__name__)
manager = Manager(app)

app.debug = True

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:mysql@localhost:3306/test?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

migrate = Migrate(app,db)

manager.add_command("db",MigrateCommand)

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    user = db.relationship("User",backref="role")

    def __repr__(self):
        return "Role:{}".format(self.name)


class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey("roles.id"))

    def __repr__(self):
        return "User:{}".format(self.username)


if __name__ == '__main__':
    manager.run()
