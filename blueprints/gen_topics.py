# 创建消息主题
# 主题格式：root/设备ID/opt
# 例如：root/123456/opt

# 生成主题
def gen_topics(deviceId):
    topic = 'root/' + str(deviceId) + '/'+'opt'
    return topic
