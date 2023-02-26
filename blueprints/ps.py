from flask import Blueprint, render_template, request, redirect, url_for, g

from exts import db
from .forms import DeviceForm, MessageForm, ControlForm,FactoryForm
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
        factorys = FactoryModel.query.all()
        return render_template('control.html', factorys=factorys)
    else:
        form = ControlForm(request.form)
        if form.validate():
            factoryName = form.factoryName.data
            control = form.control.data
            opt = form.opt.data
            # 获取操作设备列表
            controlList = control.split(' ')
            # 验证工厂ID是否存在
            factory = FactoryModel.query.filter(FactoryModel.name == factoryName).first()
            flag = 0
            if factory:
                factory_id = factory.id
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

# 控制设备顺序s
@bp.route('/ps/controls/', methods=['GET', 'POST'])
@login_require
def control_devices():
    if request.method == 'GET':
        devicesNum = request.args.get('devicesNum')
        # if devicesNum:
        #     return render_template('controls.html', devicesNum=devicesNum)
        # else:
        #     return render_template('controls.html')
        if devicesNum and devicesNum.isdigit():

            # 获取所有设备
            devices = DeviceModel.query.all()
            return render_template('controls.html', devicesNum=int(devicesNum), devices=devices)
        else:
            return render_template('controls.html', devicesNum=None)
        # return render_template('controls.html', devicesNum=devicesNum)

    else:
        # # 输入验证
        # form = ControlsForm(request.form)
        # if form.validate():
        #     return control_devices2(form.devicesNum.data)
        return 'OK'

# 添加设备
@bp.route('/ps/device/add', methods=['GET', 'POST'])
@login_require
def device_add():
    if request.method == 'GET':
        # 获取工厂列表
        factorys = FactoryModel.query.all()

        return render_template('device_add.html', factorys=factorys)
    else:
        form = DeviceForm(request.form)
        factory_name = request.form.get('factory_name')
        # form 包含的信息有：type,name,description,factory_name,maker_id
        # maker_id 为当前用户的id: g.user.id
        if form.validate():
            device_name = form.name.data
            # 验证设备是否存在
            device = DeviceModel.query.filter(DeviceModel.name == device_name).first()
            if device:
                return '设备已存在'
            else:
                # 验证工厂是否存在
                factory = FactoryModel.query.filter(FactoryModel.name == factory_name).first()
                if factory:
                    # 添加设备
                    device = DeviceModel(name=device_name, type=form.type.data, description=form.description.data, factory_id=factory.id, maker_id=g.user.id)
                    db.session.add(device)
                    db.session.commit()
                    return redirect(url_for("ps.device_add"))
                else:
                    return '工厂不存在'
        else:
            print(form.errors)
            return redirect(url_for("ps.device_add"))

# 更新设备
@bp.route('/ps/device/update', methods=['GET', 'POST'])
@login_require
def device_update():
    if request.method == 'GET':
        # 获取工厂列表
        factorys = FactoryModel.query.all()
        return render_template('device_update.html', factorys=factorys)
    else:
        # 获取工厂名称
        factory_name = request.form.get('factoryName')
        # 获取工厂ID
        factory = FactoryModel.query.filter(FactoryModel.name == factory_name).first()
        # 获取设备在线状态
        online = request.form.get('is_online')
        if online == '在线':
            is_online = 1
        else:
            is_online = 0
        # 获取设备开机状态
        status = request.form.get('now_status')
        if status == '开机':
            now_status = 1
        else:
            now_status = 0
        # 验证设备是否存在
        device_name = request.form.get('original_name')
        device = DeviceModel.query.filter(DeviceModel.name == device_name).first()
        if device:
            # 验证form数据
            form = DeviceForm(request.form)
            if form.validate():
                # 验证是否修改设备名
                if device_name == form.name.data:
                    # 更新设备信息
                    device.type = form.type.data
                    device.description = form.description.data
                    device.factory_id = factory.id
                    device.is_online = is_online
                    device.now_status = now_status
                    db.session.commit()
                    return redirect(url_for("ps.device_update"))
                else:
                    # 验证新设备名是否存在
                    new_device = DeviceModel.query.filter(DeviceModel.name == form.name.data).first()
                    if new_device:
                        return '设备已存在'
                    else:
                        # 更新设备信息
                        device.name = form.name.data
                        device.type = form.type.data
                        device.description = form.description.data
                        device.factory_id = factory.id
                        device.is_online = is_online
                        device.now_status = now_status
                        db.session.commit()
                        return redirect(url_for("ps.device_update"))
            else:
                print(form.errors)
                return redirect(url_for("ps.device_update"))
        else:
            return '设备不存在'

# 删除设备
@bp.route('/ps/device/delete', methods=['GET', 'POST'])
@login_require
def device_delete():
    if request.method == 'GET':
        return render_template('device_delete.html')
    else:
        # 获取设备名称
        device_name = request.form.get('original_name')
        # 验证设备是否存在
        device = DeviceModel.query.filter(DeviceModel.name == device_name).first()
        if device:
            # 删除设备
            db.session.delete(device)
            db.session.commit()
            return redirect(url_for("ps.device_delete"))
        else:
            return '设备不存在'

# 添加工厂
@bp.route('/ps/factory/add', methods=['GET', 'POST'])
@login_require
def factory_add():
    if request.method == 'GET':
        return render_template('factory_add.html')
    else:
        # form 包含的信息有：name,address,description
        form = FactoryForm(request.form)
        if form.validate():
            name = form.name.data
            # 验证工厂名称是否存在
            factory = FactoryModel.query.filter(FactoryModel.name == name).first()
            if factory:
                return '工厂已存在'
            else:
                # 添加工厂
                factory = FactoryModel(name=name, address=form.address.data, description=form.description.data)
                db.session.add(factory)
                db.session.commit()
                return redirect(url_for("ps.factory_add"))

# 更新工厂
@bp.route('/ps/factory/update', methods=['GET', 'POST'])
@login_require
def factory_update():
    if request.method == 'GET':
        return render_template('factory_update.html')
    else:
        # form 包含的信息有：original_name,name,address,description
        # 验证工厂名称是否存在
        name = request.form.get('original_name')
        factory = FactoryModel.query.filter(FactoryModel.name == name).first()
        if factory:
            # 验证form数据
            form = FactoryForm(request.form)
            if form.validate():

                # 验证是否修改工厂名
                if name == form.name.data:
                    # 更新工厂信息
                    factory.address = form.address.data
                    factory.description = form.description.data
                    db.session.commit()
                    return redirect(url_for("ps.factory_update"))
                else:
                    # 验证新工厂名是否存在
                    new_factory = FactoryModel.query.filter(FactoryModel.name == form.name.data).first()
                    if new_factory:
                        return '工厂已存在'
                    else:
                        # 更新工厂信息
                        factory.name = form.name.data
                        factory.address = form.address.data
                        factory.description = form.description.data
                        db.session.commit()
                        return redirect(url_for("ps.factory_update"))
            else:
                print(form.errors)
                return redirect(url_for("ps.factory_update"))
        else:
            return '工厂不存在'

# 删除工厂
@bp.route('/ps/factory/delete', methods=['GET', 'POST'])
@login_require
def factory_delete():
    if request.method == 'GET':
        return render_template('factory_delete.html')
    else:
        # form 包含的信息有：name
        name = request.form.get('original_name')
        factory = FactoryModel.query.filter(FactoryModel.name == name).first()
        if factory:
            # 删除工厂
            db.session.delete(factory)
            db.session.commit()
            return redirect(url_for("ps.factory_delete"))
        else:
            return '工厂不存在'

# 历史消息页
@bp.route('/ps/message', methods=['GET'])
@login_require
def message_display():
    # 获取消息
    messages = MessageModel.query.order_by("create_time").all()
    return render_template('message.html',messages=messages)

# # 测试
# @bp.route('/ps/test', methods=['POST'])
# def print_messages():
#     reply = {"result": "ok", "message": "success"}
#     print("got post request: ", request.get_data())
#     return json.dumps(reply), 200

