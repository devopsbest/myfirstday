from flask import Flask, render_template,flash,request
# 引入Form基类
from flask_wtf import Form
# 引入Form元素父类
from wtforms import StringField, PasswordField
# 引入Form验证父类
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"


class LoginForm(Form):
    # 用户名
    username = StringField('username', validators=[DataRequired(message="用户名不能为空")])
    # 密码
    password = PasswordField('password', validators=[DataRequired(message="密码不能为空")])


@app.route("/index", methods=['GET', 'POST'])
def baselogin():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 判断是否是验证提交
        if username =="user" and password=="password":
            # 跳转
            flash(form.username.data + '|' + form.password.data)
            return render_template('home.html',username=username)
        else:
            message = "Failed Login"
            return render_template('index.html',message=message)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
