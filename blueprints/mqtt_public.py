import paho.mqtt.client as mqtt
import json
import config


def MqttPublic(author, content, topic):
    HOST = config.MQTT_HOST
    PORT = config.MQTT_PORT
    USERNAME = config.MQTT_USERNAME
    PASSWORD = config.MQTT_PASSWORD
    KEEPALIVE = config.MQTT_KEEPALIVE
    # 1. 创建一个mqtt客户端
    client = mqtt.Client()
    client.username_pw_set(USERNAME, PASSWORD)  # 必须设置，否则会返回「Connected with result code 4」
    # 2. 连接mqtt服务器
    client.connect(HOST, PORT, KEEPALIVE)
    # 3. 设置用户数据
    client.user_data_set(author)
    # 4. 发布消息
    dict_content = json.loads(content)
    client.publish(topic, json.dumps(dict_content))
