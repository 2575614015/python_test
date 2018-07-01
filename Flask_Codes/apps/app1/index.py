import json

from apps.app1 import app1

from flask_code_1 import *
from flask import jsonify,request,redirect,Response,make_response,render_template
# from flask_code_1 import db

@app1.route("/users",methods=["GET","POST"])
def users():
    if request.method == "GET":
        data = User.query.all()
        print(data)
        return render_template("app1/create_user.html",users=data)
    elif request.method == "POST":
        # 1.获取参数
        data = None
        data1 = None
        try:
            data = json.loads(request.get_data())
        except Exception as e:
            pass
        try:
            data1 = json.loads(request.get_json())
        except Exception as e:
            pass
        data = data or data1
        # 2. 校验参数
        if not data:
            return jsonify(code=0, errmsg="请输入正确的name")
        # 3. 处理逻辑
        name = data["name"]
        email = data["email"]
        password = data["password"]
        user = User(name=name, email=email, password=password)
        try:
            db.session.add(user)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(e)
            return json.dumps({"code":"1", "errmsg":"保存数据库失败"})
        return jsonify(code="ok", errmsg="添加数据成功")

    return "请以正确的方式发送请求"