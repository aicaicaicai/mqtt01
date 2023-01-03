# 注册登陆验证模块
import string
import random
from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify

from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

# 创建蓝图对象
bp = Blueprint('auth', __name__, url_prefix='/auth')


# 登陆视图
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print('用户不存在')
                return redirect(url_for('auth.login'))
            if check_password_hash(user.password, password):
                print('登录成功')
                # cookies
                # cookies是存储在浏览器端的一小段文本信息
                # session: 用来保存用户的登录状态
                # flask中的session是基于cookies实现的, 但是session是服务器端的, cookies是客户端的
                # 通过config.py中的SECRET_KEY来加密session
                session['user_id'] = user.id
                return redirect(url_for('ps.index'))
            else:
                print('密码错误')
                return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.login'))


# 注册视图
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 验证用户提交的邮箱和验证码正确
        # 表单验证：flask-wtf
        form = RegisterForm(request.form)
        if form.validate():
            # 验证通过
            # 将用户信息写入数据库
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
            # return jsonify({'code': 200, 'msg': 'success'})
        else:
            # return jsonify({'code': 400, 'msg': 'fail'})
            return redirect(url_for('auth.register'))

# bp.route: 如果没有指定methods, 默认是GET请求
@bp.route('/captcha/email', methods=['GET'])
def get_email_captcha():
    email = request.args.get('email')
    # 生成验证码
    source = string.digits * 4
    captcha = random.sample(source, 4)
    captcha = ''.join(captcha)
    # I/O操作, 耗时操作，cerely异步执行
    message = Message(subject='注册验证码', recipients=[email], body=f'您的验证码是: {captcha}')
    mail.send(message)
    # 存储验证码到数据库
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # RESTful API
    # {'code': 200, 'message': '验证码发送成功'}
    return jsonify({'code': 200, 'message': '', 'data': None})

# 登出
@bp.route('/logout')
def logout():
    # 删除session中的user_id
    session.clear()
    return redirect(url_for('ps.index'))
