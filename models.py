# 各个功能模块的数据库模型
from exts import db
from datetime import datetime


# 用户模型
class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)
    type = db.Column(db.Integer, default=0)  # 0:管理员 1：普通用户
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    factory_id = db.Column(db.Integer, db.ForeignKey('factory.id'))
    factory = db.relationship('FactoryModel', backref=db.backref('workers', order_by=id.desc()))


# 工厂模型
class FactoryModel(db.Model):
    __tablename__ = 'factory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    address = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


# 设备模型
class DeviceModel(db.Model):
    __tablename__ = 'device'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # factory = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=True)  # 设备类型
    name = db.Column(db.String(50), nullable=True, unique=True)  # 设备名称
    # device_model = db.Column(db.String(50), nullable=True)  # 设备型号
    # device_sn = db.Column(db.String(50), nullable=True)  # 设备序列号
    # device_ip = db.Column(db.String(50), nullable=True)  # 设备IP
    # device_port = db.Column(db.Integer, nullable=True)  # 设备端口
    description = db.Column(db.Text, nullable=True)  # 设备描述
    is_online = db.Column(db.Boolean, default=0)  # 0:离线 1：在线
    is_error = db.Column(db.Boolean, default=0)  # 0:正常 1：异常
    now_status = db.Column(db.Boolean, default=0)  # 0:关机 1:开机

    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    maker_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    factory_id = db.Column(db.Integer, db.ForeignKey('factory.id'))

    maker = db.relationship(UserModel, backref=db.backref('devices', order_by=create_time.desc()))
    factory = db.relationship(FactoryModel, backref=db.backref('devices', order_by=create_time.desc()))


class MessageModel(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    # # 外键
    # device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    # author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # # 关系
    # device = db.relationship(DeviceModel, backref=db.backref('messages', order_by=create_time.desc()))
    # author = db.relationship(UserModel, backref=db.backref('messages', order_by=create_time.desc()))


# 验证码模型
class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
