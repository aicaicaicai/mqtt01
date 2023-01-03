# 创建消息主题
# 主题格式：root/工厂ID/设备ID
# 例如：root/123456/123456789

# 生成主题
def gen_topic(factor_id, device_id):
    topic = 'root/' + str(factor_id) + '/' + str(device_id)
    return topic
