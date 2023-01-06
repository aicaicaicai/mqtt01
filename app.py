from flask import Flask, session, g
from flask_migrate import Migrate
from exts import db, mail
from blueprints.auth import bp as auth_bp
from blueprints.ps import bp as ps_bp
from blueprints.ms import bp as ms_bp
from blueprints.gs import bp as gs_bp
from models import UserModel
import config

app = Flask(__name__)
# 绑定config配置文件, 从config.py中读取配置信息
app.config.from_object(config)

# 初始化db对象, 绑定app
db.init_app(app)
# 初始化mail对象, 绑定app
mail.init_app(app)

# 数据库迁移
migrate = Migrate(app, db)

# blueprints: 用来作模块化开发
# 注册蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(ps_bp)
app.register_blueprint(ms_bp)
app.register_blueprint(gs_bp)


@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)  # 从数据库中获取用户信息
        setattr(g, 'user', user)  # g是一个全局变量, 用来保存用户的登录状态
    else:
        setattr(g, 'user', None)


@app.context_processor
def my_context_processor():
    return {'user': g.user}


if __name__ == '__main__':
    app.run()
