import qrcode


img = qrcode.make('http://120.78.227.227/test_api/')
img.save('./qr.png')