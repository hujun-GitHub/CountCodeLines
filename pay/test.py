import wx
import urllib.request
import os
import file_op
import requests
import sys
import pay.pay_tool
sys.path.append("..")
import ccl_op
import config_ini_op


class Frame(wx.Frame):
    """Frame class that displays an image."""
    txt_line = ''
    parent = None
    def __init__(self, image, parent=None, id=-1,
                 pos=wx.DefaultPosition, title='Hello, wxPython!'):
        """Create a Frame instance and display image."""
        print('test.py.Frame.init:{},txt_line:{}'.format(image, self.txt_line))
        temp = image.ConvertToBitmap()
        size = temp.GetWidth(), temp.GetHeight()
        wx.Frame.__init__(self, parent, id, title, pos, size)
        self.panel = wx.Panel(self)

        self.btn = wx.Button(self.panel, label='完成支付', pos=(0, 325), size=(150, 75))
        self.btn.Bind(event=wx.EVT_BUTTON, handler=self.on_exist)
        btn1 = wx.Button(self.panel, label='取消支付', pos=(150, 325), size=(150, 75), name='cancel')
        btn1.Bind(event=wx.EVT_BUTTON, handler=self.on_cancel)

        self.bmp = wx.StaticBitmap(parent=self.panel, bitmap=temp)
        self.SetClientSize(size)

        self.txt = wx.StaticText(self.panel, label='', pos=(0, 300), size=(300, 30))
        font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.txt.SetFont(font)

    def on_exist(self, event):
        print('完成支付，修改ccl文件状态。')
        ccl_op.modify_after_pay(event.EventObject.GetName())
        wx.MessageBox("支付状态修改成功！")
        self.Close(True)
        self.parent.Destroy()
        frm = pay.pay_tool.PayFrame(None, title='支付小工具')
        frm.Show()


    def on_cancel(self, event):
        print("取消支付。")
        self.Close(True)
        self.Destroy()

    def set_btn_name(self, txt_line, parent):
        print('test.py.Frame.set_btn_name:' + txt_line + " " + str(parent))
        self.btn.SetName(txt_line)
        code_line = txt_line.split('_')[4]
        suffix = txt_line.split('_')[5]
        pay_rate = config_ini_op.get_config_value(os.path.join(os.path.join(os.getcwd(), '..'),'config.ini'),'{}_pay_rate'.format(suffix))
        pay_money = round(float(pay_rate) * int(code_line), 1)
        self.txt.SetLabel('需支付金额: {}元'.format(pay_money))
        self.parent = parent


class App(wx.App):
    """Application class."""
    def OnInit(self):
        print('test.App.OnInit:')
        host_name = file_op.get_host_name()
        url = 'http://120.78.227.227/get_pay_img_api?computer_name=' + host_name

        print('通过计算机名去找收款码图片:' + url)
        r = requests.get(url)
        print('服务器返回：' + str(r.json()))
        pay_img = r.json().get('result')
        if pay_img == '':
            wx.MessageBox("用户没有上传付款二维码")
            return False

        print('先在本地找程序员付款二维码')
        image_path = os.path.join(os.getcwd(), 'images') + '/' + pay_img
        if file_op.is_file_exist(image_path):
            print('二维码存在:' + image_path)
        else:
            print("不存在，则获取服务器付款图片:" + 'http://120.78.227.227/static/upload/' + pay_img)
            urllib.request.urlretrieve('http://120.78.227.227/static/upload/' + pay_img, filename=image_path)
            print('保存图片：' + image_path)

        image = wx.Image(image_path, wx.BITMAP_TYPE_JPEG)
        image = image.Scale(300, 400)

        self.frame = Frame(image)
        self.frame.Show()
        self.SetTopWindow(self.frame)

        print('图片展示结束')
        return True

    def set_txt_line(self, txt_line, parent):
        print('test.py.App.set_txt_line:' + txt_line)
        self.frame.set_btn_name(txt_line,parent)


def main():
    app = App('dddddddddddd')
    #app.MainLoop()


if __name__ == '__main__':
    main()
