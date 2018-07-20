import configparser
import os

def get_config_value(key):
    conf = configparser.ConfigParser()
    conf.read('config.ini')  # 文件路径
    value = conf.get("sec_a", key)  # 获取指定section 的option值
    return value


if __name__ == '__main__':
    print(get_config_value('supported_suffix'))
