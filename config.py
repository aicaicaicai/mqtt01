# 存储配置文件

# session加盐密钥
SECRET_KEY = "mdofckc%emqxflask;ok"

# 数据库配置信息
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'mqttc01'
USERNAME = 'root'
PASSWORD = 'Syj123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# 88邮箱密码：IKG5Fp6QiGmauehM
# 邮箱配置
MAIL_SERVER = "smtp.88.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "ckc888@88.com"
MAIL_PASSWORD = "IKG5Fp6QiGmauehM"
MAIL_DEFAULT_SENDER = "ckc888@88.com"

# mqtt配置
MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883
MQTT_USERNAME = "0"
MQTT_PASSWORD = "public"
MQTT_KEEPALIVE = 5

MQTT_TOPIC = "root/#"

# 线程池大小
PROCESS_NUM = 10


# EMQX配置
# API Key =
# Secret Key =