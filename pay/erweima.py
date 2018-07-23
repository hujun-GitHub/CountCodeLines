import qrcode
import file_op
import wx
import os
import requests


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
        url = 'http://120.78.227.227/is_pay_info_exist?computer_name=' + host_name
        print('判断用户是否已经上传付款二维码:' + url)
        r = requests.get(url)
        if r.json().get('result') == 'EXIST':
            print('用户已经上传。')
            return True

        print('用户未上传,生成上传路径二维码:' + 'http://120.78.227.227/test_api?computer_name=' + host_name)
        img = qrcode.make('http://120.78.227.227/test_api?computer_name=' + host_name)
        img.save('./images/qr.png')
        print('保存二维码:' + './images/qr.png')
        image = wx.Image(os.path.join(os.getcwd(), 'images') + '/qr.png', wx.BITMAP_TYPE_PNG)
        image = image.Scale(300, 300)
        self.frame = Frame(image)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        print('展示二维码')
        return True

if __name__ == '__main__':
    app = App()
    app.MainLoop()



