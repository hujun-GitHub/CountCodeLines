import qrcode
import file_op
import wx
import os

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
        # 判断是否存在记录
        #url = 'http://120.78.227.227/get_pay_img_api/?computer_name=' + host_name
        #data = json.dumps({})
        #r = requests.get(url)

        hostname = file_op.get_host_name()
        img = qrcode.make('http://120.78.227.227/test_api?computer_name=' + hostname)
        img.save('./images/test1.png')
        # create a image object
        image = wx.Image(os.path.join(os.getcwd(), 'images') + '/test1.png', wx.BITMAP_TYPE_PNG)
        image = image.Scale(300, 300)
        self.frame = Frame(image)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

app = App()
app.MainLoop()


