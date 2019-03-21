import qrcode
from PIL import Image

qr = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=1
)
qr.add_data("python爱好部落, python爱好者的家园")
qr.make(fit=True)
img = qr.make_image()

img = img.convert("RGBA")
img_w, img_h = img.size
factor = 3
size_w = int(img_w / factor)
size_h = int(img_h / factor)

icon = Image.open("snake.png")
icon_w, icon_h = icon.size
if icon_w > size_w:
    icon_w = size_w
if icon_h > size_h:
    icon_h = size_h
icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

w = int((img_w - icon_w) / 2)
h = int((img_h - icon_h) / 2)
img.paste(icon, (w, h), icon)
img.save("snake_love_qrcode.png")