# 消息发布模块
from flask import Blueprint, render_template, request, redirect, url_for, g

from exts import db
from .forms import DeviceForm, MessageForm, ControlForm
from models import DeviceModel, MessageModel, FactoryModel
from decorators import login_require
from .mqtt_public import MqttPublic
from .make_control import make_control

import json

# 创建蓝图对象
bp = Blueprint('ps', __name__, url_prefix='/')


# 首页
@bp.route('/')
def index():
    devices = DeviceModel.query.order_by(DeviceModel.update_time.desc()).all()
    return render_template('index.html', devices=devices)


# 发布消息
@bp.route('/ps/public', methods=['GET', 'POST'])
@login_require
def public_message():
    if request.method == 'GET':
        return render_template('public.html')
    else:
        form = MessageForm(request.form)
        if form.validate():
            topic = form.topic.data
            content = form.content.data
            # 获取用户名
            username = g.user.username
            MqttPublic(content=content, author=username, topic=topic)
            # 将消息写入数据库
            # message = MessageModel(content=content, author=g.user, topic=topic)
            # db.session.add(message)
            # db.session.commit()
            return redirect(url_for("ps.public_message"))
        else:
            print(form.errors)
            return redirect(url_for("ps.public_message"))


# 控制设备开机顺序
@bp.route('/ps/control', methods=['GET', 'POST'])
@login_require
def control_device():
    if request.method == 'GET':
        return render_template('control.html')
    else:
        form = ControlForm(request.form)
        if form.validate():
            factory_id = form.factory_id.data
            control = form.control.data
            opt = form.opt.data
            # 获取操作设备列表
            controlList = control.split(' ')
            # 验证工厂ID是否存在
            factory = FactoryModel.query.filter(FactoryModel.id == factory_id).first()
            flag = 0
            if factory:
                # 验证设备是否存在
                for device in controlList:
                    device = DeviceModel.query.filter(DeviceModel.id == device).first()
                    if device:
                        # 验证设备是否属于该工厂
                        if device.factory_id == factory_id:
                            # 验证设备是否在线
                            if device.is_online == 1:
                                flag = 1
                            else:
                                return '设备不在线'
                        else:
                            return '设备不属于该工厂'
                    else:
                        return '设备不存在'
            if flag == 1:
                # 发布消息
                make_control(factory_id, control, opt)
                return redirect(url_for("ps.control_device"))
        else:
            print(form.errors)
            return redirect(url_for("ps.control_device"))

# # 测试
# @bp.route('/ps/test', methods=['POST'])
# def print_messages():
#     reply = {"result": "ok", "message": "success"}
#     print("got post request: ", request.get_data())
#     return json.dumps(reply), 200

