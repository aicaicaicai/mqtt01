# 消息接收模块
from flask import Blueprint, render_template, request, redirect, url_for
from exts import db
from models import MessageModel
# from .forms import MessageForm


import json

# 创建蓝图对象
bp = Blueprint('ms', __name__, url_prefix='/')

# mqtt桥接消息接收
@bp.route('/ms/receive', methods=['POST'])
def mqtt_receive():
    reply = {"result": "ok", "message": "success"}
    # got post request: b'{"username":"0","topic":"root/1/2","timestamp":1671960862900,"qos":0,"publish_received_at":1671960862900,"pub_props":{"User-Property":{}},"peerhost":"192.168.31.170","payload":"{\\"LightSwitch9\\": \\"1\\"}","node":"emqx@127.0.0.1","metadata":{"rule_id":"rule_3uxb"},"id":"0005F0A3B94FC0FCF443000042CC0003","flags":{"retain":false,"dup":false},"event":"message.publish","clientid":"MzA4NDIyMzQxMzkxNzIyNjI4NDAzNjg2Nzg3OTUyMTQ4NDI"}'
    #
    ori_data = request.get_data()
    dict_data = json.loads(ori_data)

    topic = dict_data['topic']
    content = dict_data['payload']


    # 将消息写入数据库
    message = MessageModel(content=content, topic=topic)
    db.session.add(message)
    db.session.commit()

    print("got post request: ", dict_data)
    return json.dumps(reply), 200