'''
V8.180516: 发送微信消息
V7.180515: 发送微信消息2
v6.180510: 文件记录数据
v5.180509: 代码增量实现
v4.180508: 后台服务实现
v3.180508: 命令行参数实现
v2.180508: 函数递归实现
v1.180507: 复用函数实现
v0.180507: 流程语句实现
'''

import sys
import os
import time
import datetime
import codecs
import wx_op
import file_op
import socket
import git



def main():
	print('===> 代码行数计数程序开始')
	push_code = 0
	sum = 0
	hostname = get_host_name()
	git_base_path = get_git_base_path()

	print('===> 计算git根目录下所有.py文件的代码行数')
	code_total = file_op.count_code(git_base_path)
	print('代码行数为：' + str(code_total))
	comment_total = file_op.count_comment(git_base_path)
	print('注释行数为：' + str(comment_total))
	newline_total = file_op.count_newline(git_base_path)
	print('空白行数为：' + str(newline_total))

	# 在windows平台下，使用系统的记事本以UTF-8编码格式存储了一个文本文件，
	# 但是由于Microsoft开发记事本的团队使用了一个非常怪异的行为来保存UTF-8编码的文件，
	# 它们自作聪明地在每个文件开头添加了0xefbbbf（十六进制）的字符，
	# 所以我们就会遇到很多不可思议的问题，比如，网页第一行可能会显示一个“？”，
	# 明明正确的程序一编译就报出语法错误，等等。
	# 可以使用 Sublime Text 编辑器-文件-保存编码-utf-8

	print('===> 计算ccl文件代码行数')
	ccl_file_curr_user = git_base_path + '/' + hostname + '.ccl'
	ccl_code_total, ccl_comment_total, ccl_newline_total = count_ccl(ccl_file_curr_user, git_base_path)
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
	write_user_ccl(ccl_file_curr_user, push_code, push_newline, push_comment)
	print("ccl文件信息写入完毕。")

	print("===> 自动git add程序员的ccl文件");
	repo = git.Repo(git_base_path)
	repo.git.add(ccl_file_curr_user)
	print(ccl_file_curr_user + "文件自动add完毕。")


def write_user_ccl(ccl_file_curr_user, push_code, push_newline, push_comment):
	file = codecs.open(ccl_file_curr_user, 'r', encoding=file_op.get_encoding(ccl_file_curr_user))
	file.seek(0)
	file_lines = file.readlines();
	lastyear = 0
	lastmonth = 0
	lastday = 0
	old_push_code = 0
	old_push_newline = 0
	old_push_comment = 0
	pay_status = 0
	if len(file_lines) > 0:
		index_last_line = file_op.find_last_line_index(file_lines)
		col = file_lines[index_last_line].split(',')
		lastyear = col[0]
		lastmonth = col[1]
		lastday = col[2]
		old_push_code = int(col[5])
		old_push_newline = int(col[3])
		old_push_comment = int(col[4])
		pay_status = col[6]
	curr_year = datetime.datetime.now().year
	curr_month = datetime.datetime.now().month
	curr_day = datetime.datetime.now().day
	if curr_year == int(lastyear) and curr_month == int(lastmonth) and curr_day == int(lastday):
		file_lines[index_last_line] = '{},{},{},{},{},{},{}'.format(
			curr_year, curr_month, curr_day, old_push_newline + push_newline, old_push_comment + push_comment,
											 old_push_code + push_code, pay_status)
		print("修改" + file_lines[index_last_line])
	else:
		add_line = '{},{},{},{},{},{},{}\n'.format(year, month, day, push_newline, push_comment, push_code, 0)
		file_lines.append(add_line)
		print("添加：" + add_line)
	print("ccl文件修改后为：" + str(file_lines))
	file = open(ccl_file_curr_user, 'w', encoding='utf8')
	file.writelines(file_lines)
	file.flush()
	# 不关闭，就不能读
	file.close()


def count_ccl(ccl_file_curr_user, git_base_path):
	file_exist = os.path.exists(ccl_file_curr_user)
	if not file_exist:
		print('程序员ccl文件不存在，创建文件。' + ccl_file_curr_user)
		file = open(ccl_file_curr_user, 'w', encoding='utf8')
		file.close()
	ccl_code_total = 0
	ccl_newline_total = 0
	ccl_comment_total = 0
	for filename in os.listdir(git_base_path):
		filename = git_base_path + '/' + filename
		if os.path.isfile(filename) and filename.endswith('.ccl'):
			# print('处理文件：' + filename)
			f = codecs.open(filename, 'r', encoding=file_op.get_encoding(filename))
			f.seek(0)
			file_lines = f.readlines()
			for line in file_lines:
				if len(line.strip()) == 0:
					continue
				col = line.split(',')
				ccl_newline_total += int(col[3])
				ccl_comment_total += int(col[4])
				ccl_code_total += int(col[5])
	return ccl_code_total, ccl_comment_total, ccl_newline_total


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


def get_host_name():
	hostname = socket.gethostname()
	if '.local' in hostname:
		print("mac会出现两个hostname，一个正确的，还有一个加local的。修复：去掉local")
		hostname = hostname.replace('.local', '')
	print('程序员主机名:' + hostname)
	return hostname

if __name__ == '__main__':
	main()