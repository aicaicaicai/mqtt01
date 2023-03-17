# 控制设备定时上传信息

# 消息主题：/device/upload
# 消息内容：{“upload”:”start”}

import time
from blueprints.mqtt_public import MqttPublic

# 发布设备上传信息
def PublicDeviceUpload():
        while True:
                MqttPublic('system', '{"upload":"start"}', '/device/upload')
                print('采集设备信息...')
                time.sleep(300)

if __name__ == '__main__':
        PublicDeviceUpload()