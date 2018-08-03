"""
V8.180516: 发送微信消息
V7.180515: 发送微信消息2
v6.180510: 文件记录数据
v5.180509: 代码增量实现
v4.180508: 后台服务实现
v3.180508: 命令行参数实现
v2.180508: 函数递归实现
v1.180507: 复用函数实现
v0.180507: 流程语句实现
"""


import file_op
import git
import ccl_op
import git_op
import config_ini_op


def main():
    supported_suffix_string = str(config_ini_op.get_config_value('supported_suffix'))
    supported_suffix_arr = supported_suffix_string.split(',')
    for supported_suffix in supported_suffix_arr:
        main_process(supported_suffix[1:])


def main_process(suffix):
    char_comment = config_ini_op.get_config_value(suffix + '_comment')
    hostname = file_op.get_host_name()
    git_base_path = git_op.get_git_base_path()
    print('===> 计算git根目录下所有{}文件的代码行数'.format(suffix))
    code_total = file_op.count_code(git_base_path, suffix)
    print('代码行数为：' + str(code_total))
    comment_total = file_op.count_comment(git_base_path, suffix, char_comment)
    print('注释行数为：' + str(comment_total))
    newline_total = file_op.count_newline(git_base_path, suffix)
    print('空白行数为：' + str(newline_total))
    if code_total == 0:
        return
    # 在windows平台下，使用系统的记事本以UTF-8编码格式存储了一个文本文件，
    # 但是由于Microsoft开发记事本的团队使用了一个非常怪异的行为来保存UTF-8编码的文件，
    # 它们自作聪明地在每个文件开头添加了0xefbbbf（十六进制）的字符，
    # 所以我们就会遇到很多不可思议的问题，比如，网页第一行可能会显示一个“？”，
    # 明明正确的程序一编译就报出语法错误，等等。
    # 可以使用 Sublime Text 编辑器-文件-保存编码-utf-8
    print('===> 计算ccl文件代码行数')
    ccl_file_curr_user = git_base_path + '/' + hostname + '.ccl'
    ccl_code_total, ccl_comment_total, ccl_newline_total = ccl_op.count_ccl(ccl_file_curr_user, git_base_path, suffix)
    print('ccl代码行数为:' + str(ccl_code_total))
    print('ccl注释行数为:' + str(ccl_comment_total))
    print('ccl空白行数为:' + str(ccl_newline_total))
    print('===> 计算程序员提交代码行数(total - ccl)')
    push_code = code_total - ccl_code_total
    print("代码行数：" + str(push_code))
    push_newline = newline_total - ccl_newline_total
    print("空白行数：" + str(push_newline))
    push_comment = comment_total - ccl_comment_total
    print("注释行数：" + str(push_comment))

    print("===> 将程序员提交信息写入ccl文件")
    ccl_op.write_user_ccl(ccl_file_curr_user, push_code, push_newline, push_comment, suffix)
    print("ccl文件信息写入完毕。")
    print("===> 自动git add程序员的ccl文件");
    repo = git.Repo(git_base_path)
    repo.git.add(ccl_file_curr_user)
    print(ccl_file_curr_user + "文件自动add完毕。")

    print("===>将代码行数统计信息写入数据库")
    ccl_op.write_to_db(hostname, suffix, push_code, push_newline, push_comment)
    print("代码行数入库完毕。")

if __name__ == '__main__':
    main()

