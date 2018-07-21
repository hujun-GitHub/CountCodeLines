import datetime
import codecs
import file_op
import os


def write_user_ccl(ccl_file_curr_user, push_code, push_newline, push_comment, suffix):
    file = codecs.open(ccl_file_curr_user, 'r', encoding=file_op.get_encoding(ccl_file_curr_user))
    file.seek(0)
    file_lines = file.readlines()
    last_year = 0
    last_month = 0
    last_day = 0
    old_push_code = 0
    old_push_newline = 0
    old_push_comment = 0
    pay_status = 0
    file_type = ''
    if len(file_lines) > 0:
        print('file_lines='+str(file_lines))
        index_last_line = file_op.find_last_line_index(file_lines, suffix)
        print("index_last_line=" + str(index_last_line))
        if index_last_line is not None:
            col = file_lines[index_last_line].split(',')
            last_year = col[0]
            last_month = col[1]
            last_day = col[2]
            old_push_comment = int(col[4])
            old_push_newline = int(col[3])
            old_push_code = int(col[5])
            pay_status = col[6]
            file_type = col[7]
    curr_year = datetime.datetime.now().year
    curr_month = datetime.datetime.now().month
    curr_day = datetime.datetime.now().day
    print('suffix = {} file_type={}'.format(suffix, file_type))
    if curr_year == int(last_year) and curr_month == int(last_month) and curr_day == int(last_day) and file_type.find(suffix) >= 0:
        file_lines[index_last_line] = '{},{},{},{},{},{},{},{}\r'.format(
            curr_year, curr_month, curr_day, old_push_newline + push_newline, old_push_comment + push_comment, old_push_code + push_code, pay_status, suffix)
    else:
        add_line = '{},{},{},{},{},{},{},{}\r'.format(curr_year, curr_month, curr_day, push_newline, push_comment, push_code, 0, suffix)
        # \n系统会转成\r\n,下一次又转一次，所有换行会越来越多，用\r就不会转了。
        file_lines.append(add_line)
    print("ccl文件修改后为：" + str(file_lines))
    file = open(ccl_file_curr_user, 'w', encoding='utf8')
    file.writelines(file_lines)
    file.flush()
    # 不关闭，就不能读
    file.close()


def count_ccl(ccl_file_curr_user, git_base_path, suffix):
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
                if col[7].find(suffix) >= 0:
                    ccl_newline_total += int(col[3])
                    ccl_comment_total += int(col[4])
                    ccl_code_total += int(col[5])
    return ccl_code_total, ccl_comment_total, ccl_newline_total


def modify_after_pay(line):
    print('ccl_op.modify_after_pay:' + line)
    arr_line = line.split("_")
    filename = arr_line[0] + '.ccl'
    year = arr_line[1]
    month = arr_line[2]
    day = arr_line[3]
    file_type = arr_line[5]
    print('读取ccl文件：' + filename)
    file = codecs.open("../" + filename, 'r', encoding=file_op.get_encoding("../" + filename))
    file.seek(0)
    file_lines = file.readlines()

    print('根据当前点击这行的年月日、文件类型去确定修改文件的哪一行:')
    for index in range(len(file_lines)):
        print('第{}行:{}'.format(index, str(file_lines[index])))
        arr = file_lines[index].split(',')
        if arr[0] == year and arr[1] == month and arr[2] == day and arr[7].find(file_type) != -1:
            print('修改之前:' + str(arr))
            file_lines[index] = '{},{},{},{},{},{},{},{}'.format(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], 1, arr[7])
            print('修改之后:' + str(file_lines[index]))
    print('回写文件')
    file = open("../" + filename, 'w', encoding='utf8')
    file.writelines(file_lines)
    file.flush()
    # 不关闭，就不能读
    file.close()
    print('ccl_op.modify_after_pay over')