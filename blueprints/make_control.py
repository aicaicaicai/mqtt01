# MQTT发送消息
import json
from .gen_topic import gen_topic
from exts import connect_mqtt
import time


# 设备开机
def DeviceON(Factory_id, Device_id, control_seq):
    # 开机报文
    # msg = {"LightSwitch#": "1", "control_seq": "1 2 3 4 5 6"}
    # 获取主题
    topic = gen_topic(Factory_id, Device_id)
    # 设备名
    Device = "LightSwitch" + str(Device_id)
    msg = {Device: "1", "control_seq": control_seq}
    # 连接mqtt服务器
    client = connect_mqtt()
    # 3. 发布消息
    client.publish(topic, json.dumps(msg))
    # 关闭连接
    client.disconnect()


# 设备关机
def DeviceOFF(Factory_id, Device_id, control_seq):
    # 关机报文
    # msg = {"LightSwitch#": "0", "control_seq": "1 2 3 4 5 6"}
    # 获取主题
    topic = gen_topic(Factory_id, Device_id)
    # 设备名
    Device = "LightSwitch" + str(Device_id)
    msg = {Device: "0", "control_seq": control_seq}
    # 连接mqtt服务器
    client = connect_mqtt()
    # 3. 发布消息
    client.publish(topic, json.dumps(msg))
    # 关闭连接
    client.disconnect()


def make_control(Factory_id, control, opt):
    if opt == 1:
        controlList = control.split(' ')
        for Device_id in controlList:
            DeviceON(Factory_id, Device_id, control)
            time.sleep(1)
    else:
        controlList = control.split(' ')
        for Device_id in controlList:
            DeviceOFF(Factory_id, Device_id, control)
            time.sleep(1)
