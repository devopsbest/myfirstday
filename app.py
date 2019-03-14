from flask import Flask, render_template,flash,request,redirect,url_for
# 引入Form基类
from flask_wtf import Form
# 引入Form元素父类
from wtforms import StringField, PasswordField,SubmitField
# 引入Form验证父类
from wtforms.validators import DataRequired
from exts import db

from flask_sqlalchemy import SQLAlchemy
import pymysql
from models import User


app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"

#配置flask配置对象中键：SQLALCHEMY_DATABASE_URI

#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://username:password@hostname/database"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/testflask?charset=utf8'

#配置flask配置对象中键：SQLALCHEMY_COMMIT_TEARDOWN,设置为True,应用会自动在每次请求结束后提交数据库中变动

app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

#获取SQLAlchemy实例对象，接下来就可以使用对象调用数据

# db = SQLAlchemy(app)
db.init_app(app)


class LoginForm(Form):
    # 用户名
    username = StringField('用户名:', validators=[DataRequired(message="用户名不能为空")])
    # 密码
    password = PasswordField('密码:', validators=[DataRequired(message="密码不能为空")])

    submit = SubmitField('提交')

class RegisterForm(Form):
    # 用户名
    username = StringField('用户名:', validators=[DataRequired(message="用户名不能为空")])
    # 邮箱
    email = StringField('邮箱:', validators=[DataRequired(message="邮箱不能为空")])
    # 密码
    password = PasswordField('密码:', validators=[DataRequired(message="密码不能为空")])

    submit = SubmitField('提交')


@app.route("/index", methods=['GET', 'POST'])
def baselogin():
    login_form = LoginForm()
    # 逻辑处理
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        # 判断是否是验证提交
        if login_form.validate_on_submit():
            if username =="user" and password=="password":
                # 跳转
                message = "welcome user {}".format(login_form.username.data)
                return render_template('home.html',message=message)
            else:
                message = "Failed Login"
                return render_template('index.html',form=login_form,message=message)

    return render_template('index.html',form=login_form)


@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    # 逻辑处理
    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        # 判断是否是验证提交
        if register_form.validate_on_submit():
            newobj = User(username=username, email=email, password=password)
            db.session.add(newobj)
            db.session.commit()
            message = "注册成功"
            flash(message)
            render_template("register.html",form=register_form)


    return render_template("register.html",form=register_form)

@app.route("/all", methods=['GET', 'POST'])
def show():
    users = User.query.all()
    flash("都在这里了")
    return render_template("show.html",users=users)


if __name__ == '__main__':
    app.run(debug=True)
