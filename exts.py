# 其他共同使用的功能
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# 定义空的db对象
db = SQLAlchemy()
# 配置email
mail = Mail()

# MQTT发送消息
import paho.mqtt.client as mqtt
import config


# 连接mqtt服务器
def connect_mqtt():
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
    return client
