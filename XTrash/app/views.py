# -*- coding: UTF-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
import _thread as thread
import requests
from urllib.parse import urljoin

import datetime
import traceback
import random
import os
import json
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

import sched,time
import threading
from .models import QRcodeModels
from .models import User
from .createImage import CreateImage
from views import settings
from django.http import HttpResponse, HttpResponseRedirect


HOST = "www.yikeni.com"
PORT = 1883
#  pip install paho-mqtt

# Create your views here.

def upload(request):

    qr = QRcodeModels()

    createImage = CreateImage()

    settings.number = settings.number + 1

    imgPath = createImage.getQrPath(str(settings.number), settings.number)


    print(imgPath)

    return render(request, 'upload.html', {"imgId": imgPath})


def getQrImageName(request):

    qr = QRcodeModels()

    createImage = CreateImage()

    settings.number = settings.number + 1

    imgPath = createImage.getQrPath(str(settings.number), settings.number)
    print(imgPath)
    return HttpResponse(imgPath)


#http://localhost:8080/openforqr/?qrCode=1
def openForQR(request):

    qrCode = request.GET.get('qrCode')
    nickName = request.GET.get('nickName')

    qrCode = int(qrCode)
    print(qrCode)



    client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    client = mqtt.Client(client_id)  # ClientId不能重复，所以使用当前时间
    client.username_pw_set("secomiot", "#secom&2019@")  # 必须设置，否则会返回「Connected with result code 4」
    client.connect(HOST, PORT, 60)
    client.loop_start()

    jsonStr = {"type": "login", "userId": 12345, "usrname": nickName, "result": 1, "message": "登录成功"}
    jsonStr = json.dumps(jsonStr)

    client.publish("xtrash/0001",
                   jsonStr)  # client2 publishes topic 'manipulated' with content 'i*0.02'

    client.loop_stop()


    if qrCode%2 ==0:
        return HttpResponse(0)
    else:
        return HttpResponse(1)

def getQrImage(request):

    qr = QRcodeModels()

    createImage = CreateImage()

    settings.number = settings.number + 1

    imgName = createImage.getQrPath(str(settings.number), settings.number)


    print(imgName)

    t = threading.Thread(target=deleteFile, args=(imgName,))
    t.start()

    imagepath = os.path.join(settings.BASE_DIR, "image/{}".format(imgName))  # 图片路径
    with open(imagepath, 'rb') as f:
        image_data = f.read()

    return HttpResponse(image_data, content_type="image/png")

def deleteFile(file):

    time.sleep(7)
    print("  ------  delete file !")
    imagepath = os.path.join(settings.BASE_DIR, "image/{}".format(file))  # 图片路径
    os.remove(imagepath)

    print(file)


def home(request):
    userName = 'admin'
    password = '123456'

    count = User.objects.filter(userName=userName, password=password).count()

    if count > 0:
        print("======> ")
    else:

        updateTime = datetime.datetime.now()

        userDB = User()
        userDB.userName = userName
        userDB.password = password
        userDB.remarks = ""

        try:
            userDB.save()
        except FieldError as fieldErr:
            print(traceback.print_exc())
            raise FieldError(fieldErr)
        except Exception as e:
            print(traceback.print_exc())
            raise Exception(e)


    return HttpResponse("--------------------------------------------------" +
                        "--------------------------------------------------" +
                        " Welcome to iVideo test page ! " +
                        "---------------------------------------" +
                        "---------------------------------------")

#http://localhost:8080/get_qrContent/?deviceId="001"
def getQrContentTrash(request):

    device = request.GET.get('deviceId')
    token = 12345

    jsonStr = {'token': token, 'qrid': device}

    print(jsonStr)

    return HttpResponse(json.dumps(jsonStr))

# http://localhost:8080/add_operationecord/?deviceId="123"&type="1"&userId="122"&token='1234'
def addOperationRecordTrash(request):

    deviceId = request.GET.get('deviceId')

    type = request.GET.get('type')

    userId = request.GET.get('userId')
    token = request.GET.get('token')

    print(deviceId)
    print(type)
    print(userId)
    print(token)

    return HttpResponse(1)


#http://localhost:8080/upload_picture/?deviceId="001"&token='1234'&type='1'&userId="122"
def uploadPictureTrash(request):

    deviceId = request.GET.get('deviceId')
    type = request.GET.get('type')
    token = request.GET.get('token')
    userId = request.GET.get('userId')

    print(token)

    print(deviceId)
    print(type)

    file = request.FILES.get('images')
    files = request.FILES.getlist('images')

    for file in files:

        fileName = file.name
        img_path = os.path.join('image/picture/', fileName)

        print(img_path)

        print(" saveImage  " + img_path)
        with open(img_path, 'wb') as f:
            for item in file.chunks():
                f.write(item)
            f.close()


    return HttpResponse(1)


def uploadPictureTrash1(request):

    deviceId = request.GET.get('deviceId')
    type = request.GET.get('type')
    token = request.GET.get('token')

    print(token)

    print(deviceId)
    print(type)

    file = request.FILES.get('images')

    fileName = file.name

    img_path = os.path.join('image/picture/', fileName)

    print(img_path)

    print(" saveImage  " + img_path)
    with open(img_path, 'wb') as f:
        for item in file.chunks():
            f.write(item)
        f.close()


    return HttpResponse(1)


# http://localhost:8080/upload_weight/?deviceId="001"&weight=123&token='1234'&userId="122"
def uploadWeightTrash(request):

    deviceId = request.GET.get('deviceId')
    weight = request.GET.get('weight')
    token = request.GET.get('token')

    print(token)
    print(deviceId)
    print(weight)

    return HttpResponse(1)

# http://localhost:8080/upload_height/?deviceId="001"&height=123&token='1234'
def uploadHeightTrash(request):
    deviceId = request.GET.get('deviceId')
    height = request.GET.get('height')
    token = request.GET.get('token')

    print(token)
    print(deviceId)
    print(height)

    return HttpResponse(1)

# http://localhost:8080/getCost/?deviceId="001"&token='1234'&userId="122"
def getCostTrash(request):
    deviceId = request.GET.get('deviceId')

    token = request.GET.get('token')

    print(token)

    print(deviceId)

    jsonStr = {'integral': 5, 'money':0.58,"message":"继续加油哦！ "}

    print(jsonStr)

    return HttpResponse(json.dumps(jsonStr))
