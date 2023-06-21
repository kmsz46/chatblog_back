import json
from flask import Flask,request,make_response,jsonify,session
from flask_cors import CORS
from cipher import hash
from datetime import timedelta
import config
from db.models import User,Thread,ThreadGroup,UserGroup,Response
from db.database import db,init_db
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')
init_db(app)
CORS(app)

## ユーザ登録
@app.route('/setup', methods=['POST'])
def user_register():
  user = request.get_json()
  if request.method == 'POST':
    user_info = User(
      user_name = user['name'],
      email = user['email'],
      groups = ",".join(user["group"]),
      password = hash(user['password'])
    )
    db.session.add(user_info)
    db.session.commit()

## ログイン認証
@app.route("/login",methods=["GET","POST"])
def login():
    user = request.get_json()
    user_info = db.session.query(User).filter(User.name == user["name"],
                                User.password == hash(user["password"]))
    if user_info == None:
        return False
    else:
        return user_info

## ユーザ探索
@app.route("/usersearch",methods=["GET","POST"])
def profile():
    user_id = request.get_json()["id"]
    user_data = db.get_or_404(User,user_id)
    user_blog = db.session.query(Thread).filter(Thread.user_id == user_id)
    return make_response(jsonify({"user_info":user_data,"blog_info":user_blog}))

## グループ追加
@app.route("/groupadd",methods=["GET","POST"])
def groupadd():
    user_data = request.get_json()
    user_info = db.get_or_404(User,user_data["id"])
    user_info.group = ",".join(user_data["group"])
    db.session.add(user_info)
    db.session.commit()

## 記事作成
@app.route("/blogcreate",methods=["GET","POST"])
def create():
    blog_info = request.get_json()
    blog_info["sub_tag"] = ",".join(blog_info["sub_tag"])
    db.session.add(blog_info)

## 記事更新
@app.route("/blogedit",methods=["GET","POST"])
def blogedit():
    blog_data = request.get_json()
    blog_info = db.session.query(Thread).filter(Thread.id == blog_data["id"])
    blog_info.title = blog_data["title"]
    blog_info.content = blog_data["content"]
    blog_info.group = blog_data["group"]
    blog_info.tag = blog_data["tag"]
    blog_info.open_op = blog_data["option"]
    db.session.commit()
    
# @app.route("/blog_delate",methods=["GET","POST"])
# def delate():
#     blog_title = request.get_json()
#     blog_list = json.load(open(BLOG_PATH, 'r'))
#     for blog in blog_list:
#         if blog_list["title"]==blog_title:
#             blog_list.remove(blog)
#             break

## 記事取得
@app.route("/display",methods=["GET","POST"])
def display():
    blog_list = []
    user_group = request.get_json()["groups"]
    blog_data = db.session.query(Thread).all()
    for blog in blog_data:
        if blog.group_op and set(user_group) & set(blog.group.split(",")) == set(blog.group.split(",")):
            blog_list.append(blog)
        elif not blog.group_op and set(user_group) & set(blog.group.split(",")) != set():
            blog_list.append(blog)
    return make_response(jsonify({"blog_list":blog_list}))

## 記事の内容取得
@app.route("/contents",methods=["GET","POST"])
def contents():
    blog_id = request.get_json()["id"]
    print(blog_id)
    target = db.session.query(Thread).filter(Thread.id == blog_id)
    return make_response(jsonify({"blog":target}))
    
if __name__ == "__main__":
    app.run(debug=True)
