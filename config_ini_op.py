import configparser
import os

def get_config_value(config_file_path, key):
    conf = configparser.ConfigParser()
    print("============="+os.getcwd())
    conf.read(config_file_path)  # 文件路径
    value = conf.get("sec_a", key)  # 获取指定section 的option值
    return value


if __name__ == '__main__':
    print(get_config_value('supported_suffix'))
