import requests
# 导入requests_toolbe

url = "http://localhost:8080/upload_picture/?deviceId='001'&token='1234'&type='1'"

files = {'images': open('../image/snake_qrcode1.png', 'rb')}

files = {'images': open('../image/snake_qrcode1.png', 'rb')}


multiple_files = [
    ('images', ('1.png', open('../image/snake_qrcode1.png', 'rb'), 'image/png')),
    ('images', ('2.png', open('../image/snake_qrcode2.png', 'rb'), 'image/png'))
]

headers = {
    'Api-Key':
    'InhpeWFuZzA4MDdJBtx4AWlPpI_Oxx1Ki8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
}

#r = requests.post(url, files=files, headers=headers)

r = requests.post(url, files=multiple_files, headers=headers)

print(r.text)