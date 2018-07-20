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
        print('通过计算机名去找收款码图片:' + host_name)
        url = 'http://120.78.227.227/get_pay_img_api/?computer_name=' + host_name
        data = json.dumps({})
        r = requests.get(url)
        print(r.json())
        print(r.json().get("result"))
        pay_img = r.json().get('result')
        # download image
        print("获取服务器付款图片:" + 'http://120.78.227.227/static/upload/' + pay_img)
        urllib.request.urlretrieve('http://120.78.227.227/static/upload/' + pay_img, filename='./images/' + pay_img)
        # create a image object
        image = wx.Image(os.path.join(os.getcwd(), 'images') + '/' + pay_img, wx.BITMAP_TYPE_JPEG)
        image = image.Scale(300, 400)
        self.frame = Frame(image)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True
def main():
    app = App()
    app.MainLoop()
if __name__ == '__main__':
    main()
