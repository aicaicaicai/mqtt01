from flask import Blueprint, jsonify, request

from models import DeviceModel, FactoryModel
from decorators import login_require


bp = Blueprint('gs', __name__)


# 获取工厂信息
@bp.route('/gs/factoryInfo/factoryName', methods=['GET'])
@login_require
def factory():
    factoryName = request.args.get('factoryName')
    factory = FactoryModel.query.filter(FactoryModel.name == factoryName).first()
    if factory:
        fac = {}
        fac["name"] = factory.name
        fac["id"] = factory.id
        fac["address"] = factory.address
        fac["description"] = factory.description

        # 返回ajax请求
        return jsonify({"code": 200, "message": "工厂信息获取成功！", "data": fac})
    else:
        return jsonify({"code": 400, "message": "工厂不存在", "data": {}})

# 获取设备信息
@bp.route('/gs/deviceInfo/deviceName', methods=['GET'])
@login_require
def device():
    deviceName = request.args.get('deviceName')
    device = DeviceModel.query.filter(DeviceModel.name == deviceName).first()
    if device:
        dev = {}
        dev["name"] = device.name
        dev["id"] = device.id
        dev["description"] = device.description
        dev["factoryName"] = device.factory.name
        dev["type"] = device.type
        # dev["is_online"] = device.is_online
        if device.is_online:
            dev["is_online"] = "在线"
        else:
            dev["is_online"] = "离线"
        # dev["now_status"] = device.now_status
        if device.now_status:
            dev["now_status"] = "开机"
        else:
            dev["now_status"] = "关机"
        dev["maker_name"] = device.maker.username

        # 返回ajax请求
        return jsonify({"code": 200, "message": "设备信息获取成功！", "data": dev})
    else:
        return jsonify({"code": 400, "message": "设备不存在", "data": {}})