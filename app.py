from flask import Flask, render_template,flash,request,redirect,url_for
# 引入Form基类
from flask_wtf import Form
# 引入Form元素父类
from wtforms import StringField, PasswordField,SubmitField
# 引入Form验证父类
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"


class LoginForm(Form):
    # 用户名
    username = StringField('用户名:', validators=[DataRequired(message="用户名不能为空")])
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


if __name__ == '__main__':
    app.run(debug=True)
