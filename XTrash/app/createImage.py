import qrcode

import datetime

class CreateImage(object):

    def getQrPath(self, value,number):
        now = datetime.datetime.now()

        print(now)
        print(type(now))

        time1 = now.strftime("%Y-%m-%d_%H:%S:%M")
        pathStr = 'image/' + time1 + '_' + str(number) + '.png'
        imageUrl=  time1 + '_' + str(number) + '.png'
        print(pathStr)

        # pip install qrcode
        qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=1)
        qr.add_data(value)
        qr.make(fit=True)
        img = qr.make_image()
        img.save(pathStr)

        return imageUrl

