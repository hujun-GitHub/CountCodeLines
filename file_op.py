import chardet
import os
import codecs
import socket


def count_code(path, suffix):
    i = 0   # 递归迭代函数中，函数级变量代码定义的位置不对，实现逻辑就会出错
    path_list = os.listdir(path)
    for filename in path_list:
        if os.path.isfile(path + '/' + filename):
            if filename.endswith(suffix):    # 用 endswith() 代替 in ，精确匹配，解决读取到 .pyc 文件时的编码报错问题
                encoding = get_encoding(path + '/' + filename)
                if encoding is None:
                    encoding = 'utf-8'
                f = codecs.open(path + '/' + filename, encoding=encoding)
                k = 0
                for line in f.readlines():
                    line = line.strip()
                    if not line.startswith('#') and len(line):
                        k += 1
                i += k

        if os.path.isdir(path + '/' + filename):
            current_path = path + '/' + filename
            j = count_code(current_path, suffix)
            if j:
                i = i + j
    return i    # 递归迭代函数中，return 用于从函数内部传递返回值出来；位置决定递归函数的返回结束！


def count_newline(path, suffix):
    i = 0   # 递归迭代函数中，函数级变量代码定义的位置不对，实现逻辑就会出错
    path_list = os.listdir(path)

    for filename in path_list:
        if os.path.isfile(path + '/' + filename):
            if filename.endswith(suffix):    # 用 endswith() 代替 in ，精确匹配，解决读取到 .pyc 文件时的编码报错问题
                f = codecs.open(path + '/' + filename, encoding=get_encoding(path + '/' + filename))
                k = 0
                for line in f.readlines():
                    line = line.strip()
                    if not len(line):
                        k += 1
                i += k
        if os.path.isdir(path + '/' + filename):
            current_path = path + '/' + filename
            j = count_newline(current_path, suffix)
            if j:
                i = i + j
    return i    # 递归迭代函数中，return 用于从函数内部传递返回值出来；位置决定递归函数的返回结束！


def count_comment(path, suffix, char_comment):
    i = 0   # 递归迭代函数中，函数级变量代码定义的位置不对，实现逻辑就会出错
    path_list = os.listdir(path)

    for filename in path_list:
        if os.path.isfile(path + '/' + filename):
            if filename.endswith(suffix):    # 用 endswith() 代替 in ，精确匹配，解决读取到 .pyc 文件时的编码报错问题
                f = codecs.open(path + '/' + filename, encoding=get_encoding(path + '/' + filename))
                k = 0
                for line in f.readlines():
                    line = line.strip()
                    if line.startswith(char_comment):
                        k += 1
                i += k

        if os.path.isdir(path + '/' + filename):
            current_path = path + '/' + filename
            j = count_comment(current_path, suffix, char_comment)
            if j:
                i = i + j
    return i    # 递归迭代函数中，return 用于从函数内部传递返回值出来；位置决定递归函数的返回结束！


def count_all(path, suffix):
    i = 0   # 递归迭代函数中，函数级变量代码定义的位置不对，实现逻辑就会出错
    path_list = os.listdir(path)
    for filename in path_list:
        if os.path.isfile(path + '/' + filename):
            if filename.endswith(suffix):    # 用 endswith() 代替 in ，精确匹配，解决读取到 .pyc 文件时的编码报错问题
                f = codecs.open(path + '/' + filename, encoding=get_encoding(path + '/' + filename))
                k = len(f.readlines())
                i += k
        if os.path.isdir(path + '/' + filename):
            current_path = path + '/' + filename
            j = count_all(current_path)
            if j:
                i = i + j

    return i    # 递归迭代函数中，return 用于从函数内部传递返回值出来；位置决定递归函数的返回结束！


# bug:如果文件为空, 返回时NoneType
def get_encoding(file):
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']


def find_last_line_index(lines, suffix):
    for index in range(len(lines)-1, -1, -1):
        if len(lines[index].strip()) == 0:
            continue
        else:
            if lines[index].split(',')[7].find(suffix) >= 0:
                return index


def count_code_line_txt(path):
    code_sum = 0
    for filename in os.listdir(path):
        if os.path.isfile(path + '/' + filename) and 'data' in filename:
            f = codecs.open(path + '/' + filename, 'r',
                            encoding=get_encoding(path + '/' + filename))
            f.seek(0)
            fl = f.readlines()
            # 遍历文件里每一条记录。
            for index in range(len(fl)):
                if len(fl[index].strip()) == 0:
                    continue
                code_sum += int(fl[index].split(',')[5])
                print('code_sum:' + code_sum)
    return code_sum


def get_host_name():
    hostname = socket.gethostname()
    if '.local' in hostname:
        print("mac会出现两个hostname，一个正确的，还有一个加local的。修复：去掉local")
        hostname = hostname.replace('.local', '')
    print('程序员主机名:' + hostname)
    return hostname
