import qrcode

import datetime

class CreateImage(object):

    def getQrPath(self, value):

        pathStr = 'login.png'

        # pip install qrcode
        qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=1)
        qr.add_data(value)
        qr.make(fit=True)
        img = qr.make_image()
        img.save(pathStr)


