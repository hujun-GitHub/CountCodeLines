import sys
import os


def get_git_base_path() -> object:
    system_type = sys.platform
    git_base_path = ''
    if system_type.startswith('win'):
        print('程序员的电脑是windows系统。')
        # git_base_path = os.path.abspath(os.path.join(os.getcwd(), "../../.."))
        # 本地测试用
        git_base_path = os.getcwd()
    elif system_type == 'darwin':
        print('程序员的电脑是mac系统。')
        git_base_path = os.path.abspath(os.path.join(sys.MEIPASS, "../../.."))
    else:
        print('可能是ubuntu系统,代码没有完成。')
    print("git本地根目录:" + git_base_path)
    return git_base_path
