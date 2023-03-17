# MQTT发送消息
import json
from .gen_topics import gen_topics
from exts import connect_mqtt
import time


# # 设备开机
# def DeviceON(Factory_id, Device_id, control_seq):
#     # 开机报文
#     # msg = {"LightSwitch#": "1", "control_seq": "1 2 3 4 5 6"}
#     # 获取主题
#     topic = gen_topic(Factory_id, Device_id)
#     # 设备名
#     Device = "LightSwitch" + str(Device_id)
#     msg = {Device: "1", "control_seq": control_seq}
#     # 连接mqtt服务器
#     client = connect_mqtt()
#     # 发布消息
#     client.publish(topic, json.dumps(msg))
#     # 关闭连接
#     client.disconnect()
#
#
# # 设备关机
# def DeviceOFF(Factory_id, Device_id, control_seq):
#     # 关机报文
#     # msg = {"LightSwitch#": "0", "control_seq": "1 2 3 4 5 6"}
#     # 获取主题
#     topic = gen_topic(Factory_id, Device_id)
#     # 设备名
#     Device = "LightSwitch" + str(Device_id)
#     msg = {Device: "0", "control_seq": control_seq}
#     # 连接mqtt服务器
#     client = connect_mqtt()
#     # 3. 发布消息
#     client.publish(topic, json.dumps(msg))
#     # 关闭连接
#     client.disconnect()


def make_controls(devicesNameList, devicesOptList, devicesIdList):
    # if opt == 1:
    #     controlList = control.split(' ')
    #     for Device_id in controlList:
    #         DeviceON(Factory_id, Device_id, control)
    #         time.sleep(1)
    # else:
    #     controlList = control.split(' ')
    #     for Device_id in controlList:
    #         DeviceOFF(Factory_id, Device_id, control)
    #         time.sleep(1)

    # 开机顺序
    control = ''
    for c in range(len(devicesNameList)):
        if devicesOptList[c] == "1":
            control = control + str(devicesIdList[c]) + ','
    control = control[:-1]


    # 连接mqtt服务器
    client = connect_mqtt()

    for i in range(len(devicesNameList)):
        # if devicesOptList[i] == 1:
        # DeviceON(Factory_id, devicesNameList[i], control)
        # 生成设备主题
        topic = gen_topics(devicesIdList[i])
        # 设备操作指令
        msg = {"opt": devicesOptList[i], "control_seq": control}
        # print(json.dumps(msg))
        # 发布消息
        client.publish(topic, json.dumps(msg))
        time.sleep(1)
    # 关闭连接
    client.disconnect()
    # time.sleep(1)
        # else:
        #     # DeviceOFF(Factory_id, devicesNameList[i], control)
        #
        #     time.sleep(1)
