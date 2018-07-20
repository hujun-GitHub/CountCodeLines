import wx
import urllib.request
import os
import file_op
import requests
import json


class Frame(wx.Frame):
    """Frame class that displays an image."""
    def __init__(self, image, parent=None, id=-1,
                 pos=wx.DefaultPosition, title='Hello, wxPython!'):
        """Create a Frame instance and display image."""
        temp = image.ConvertToBitmap()
        size = temp.GetWidth(), temp.GetHeight()
        wx.Frame.__init__(self, parent, id, title, pos, size)
        panel = wx.Panel(self)
        self.bmp = wx.StaticBitmap(parent=panel, bitmap=temp)
        self.SetClientSize(size)


class App(wx.App):
    """Application class."""
    def OnInit(self):
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


def main():
    app = App()
    app.MainLoop()


if __name__ == '__main__':
    main()
