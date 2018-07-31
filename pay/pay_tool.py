import wx
import codecs
import os
import sys
import test
sys.path.append("..")
import file_op
import ccl_op


class PayFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(PayFrame, self).__init__(*args, **kw, size=(1300,500))

        self.pnl = wx.Panel(self)
        self.make_main_ui()
        self.make_menu_bar()
        self.CreateStatusBar()
        self.SetStatusText("欢迎来到python世界!")

    def make_main_ui(self):
        # 遍历以ccl文件（以后这个是要改的），展示所有程序员push代码的记录。
        upper_folder = os.path.abspath(os.path.join(os.getcwd(), ".."))
        index_line = 0
        cost_money = 0
        left_money = 0
        print(upper_folder)
        wx.StaticText(self.pnl, label="成员\t\t\t\t年\t\t月\t\t日\t\t空白行\t\t注释行\t\t代码行\t\t代码总行数\t\t代码类型\t\t是否付款", pos=(30, 80), size=(1300, 30))
        dic_code_total = {}
        for filename in os.listdir(upper_folder):
            if os.path.isfile(upper_folder + '/' + filename) and filename.endswith('.ccl'):
                f = codecs.open(upper_folder + '/' + filename, 'r',
                                encoding=file_op.get_encoding(upper_folder + '/' + filename))
                f.seek(0)
                fl = f.readlines()
                # 遍历文件里每一条记录。
                for index in range(len(fl)):
                    if len(fl[index].strip()) == 0:
                        continue
                    cost_money += self.create_ui_line(filename, fl[index], index_line, dic_code_total)
                    index_line += 1
                left_money = 10000 - cost_money

        st = wx.StaticText(self.pnl, label="奖池剩余奖金：" + str(left_money), pos=(25, 25))

        font = st.GetFont()
        font.PointSize += 10
        st.SetFont(font)

    def create_ui_line(self, filename, line, line_number, code_dic_total):
        print('create_ui_line:' + line)
        arr_line = line.split(',')
        dev_name = filename.replace(".ccl", "")
        suffix = arr_line[7].strip('\r')
        label = dev_name + "_" + arr_line[0] + "_" + arr_line[1] + "_" + arr_line[2] + "_" + arr_line[3] + "_" + suffix
        if code_dic_total.get(suffix) is None:
            code_dic_total[suffix] = 0
        code_dic_total[suffix] += int(arr_line[5])
        wx.StaticText(self.pnl, label=dev_name, pos=(30, 120 + line_number * 40), size=(130, 60))
        wx.StaticText(self.pnl, label=arr_line[0], pos=(200, 120 + line_number * 40), size=(100, 60))  # year
        wx.StaticText(self.pnl, label=arr_line[1], pos=(300, 120 + line_number * 40), size=(100, 60))  # month
        wx.StaticText(self.pnl, label=arr_line[2], pos=(400, 120 + line_number * 40), size=(100, 60))  # day
        wx.StaticText(self.pnl, label=arr_line[3], pos=(500, 120 + line_number * 40), size=(100, 60))  # blank
        wx.StaticText(self.pnl, label=arr_line[4], pos=(600, 120 + line_number * 40), size=(100, 60))  # comment
        wx.StaticText(self.pnl, label=arr_line[5], pos=(700, 120 + line_number * 40), size=(100, 60))  # code
        wx.StaticText(self.pnl, label=str(code_dic_total[suffix]), pos=(800, 120 + line_number * 40), size=(100, 60))  # code_total
        wx.StaticText(self.pnl, label=suffix, pos=(960, 120 + line_number * 40), size=(100, 60))  # suffix
        # 最后一列有\t\n,所有取值是要去掉。
        if arr_line[6][0] == '0':
            btn = wx.Button(self.pnl, label='点击付款', pos=(1080, 110 + line_number * 40), size=(80, 30), name=label)
            btn.Bind(event=wx.EVT_BUTTON, handler=self.on_pay)
            return 0
        else:
            wx.StaticText(self.pnl, label='已付款' + arr_line[5] + '元', pos=(1080, 120 + line_number * 40), size=(80, 30))
            return int(arr_line[5])

    def make_menu_bar(self):
        file_menu = wx.Menu()
        hello_item = file_menu.Append(-1, "&Hello...\tCtrl-H","Help string shown in status bar for this menu item")
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT)
        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT)
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(help_menu, "&Help")
        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.on_hello, hello_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)

    def on_exit(self, event):
        self.Close(True)

    def on_hello(self, event):
        wx.MessageBox("Hello again wxPython")

    def on_about(self, event):
        wx.MessageBox("This is a wxPython Hello World sample!", "About Hello World 2", wx.OK | wx.ICON_INFORMATION)

    def on_pay(self, event):
        print('pay_tool.py.on_pay:' + event.EventObject.GetName())
        app = test.App()
        app.set_txt_line(event.EventObject.GetName(), self)
        app.MainLoop()
        print('pay_tool.py.on_pay over')

    def on_pay_(self, event):

        if not self.validate_pay():
            return

        self.Destroy()
        frm = PayFrame(None, title='支付小工具')
        frm.Show()

    def validate_pay(self):
        count_code_line_git = file_op.count_code('..')
        count_code_line_txt = file_op.count_code_line_txt('..')
        if count_code_line_txt != count_code_line_git:
            wx.MessageBox("txt代码行数{}和git提交的代码行数{}不一致!无法付款。".format(count_code_line_txt, count_code_line_git))
            return False
        return True



if __name__ == '__main__':
    app = wx.App()
    frm = PayFrame(None, title='支付小工具')
    frm.Show()
    app.MainLoop()
    #urllib.request.urlretrieve('http://120.78.227.227/static/upload/5B75C22E-39BF-4011-B66D-3D070FB75167.jpeg',filename='./images/5B75C22E-39BF-4011-B66D-3D070FB75167.jpeg')

