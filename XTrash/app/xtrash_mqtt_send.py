# coding:utf-8

import time
import threading
import json
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt





HOST = "13.229.7.162"


PORT = 1888

HOST = "www.yikeni.com"
PORT = 1883

def action(arg):

    client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    client_id = client_id + str(arg)
    client = mqtt.Client(client_id)  # ClientId不能重复，所以使用当前时间
    client.username_pw_set("secomiot", "#secom&2019@")  # 必须设置，否则会返回「Connected with result code 4」
    client.connect(HOST, PORT, 60)
    client.loop_start()

    count = 500

    while 1:

        count = count + 1
        if count>100000:
            count = 500
        print('the arg is:   ===> %s      %s' %(arg ,count))
        jsonStr = getMqttJson(count, arg)
        jsonStr = json.dumps(jsonStr)

        if arg > 50 and arg < 100:

            client.publish("xtrash/0001",
                           jsonStr)  # client2 publishes topic 'manipulated' with content 'i*0.02'

        else:

            client.publish("xtrash/0001", jsonStr)  # client2 publishes topic 'manipulated' with content 'i*0.02'

        time.sleep(5)


    client.loop_stop()




def getMqttJson(number,arg):

    jsonStr = {"type": "login", "usrname": "林公子" ,"result":1,"message":"登录成功"}


    return jsonStr

def readFile(fileName,array):
    for line in open(fileName):

        dataArray = line.split(',')
        if(len(dataArray) > 4):

            item = [dataArray[1],dataArray[3]]
            array.append(item)
           # print(item)



for i in range(1):

    t = threading.Thread(target=action,args=(i,))
    t.start()



# v1/mobile/telemetry {"jsonrpc": "2.0", "id": 1, "message": {"method": "headline", "status": {"jsonns": "commands/objects/status", "object": {"object_type": "device", "object_id": "Vehicle_001", "owner_id": "", "meta": {"device_type": "Vehicle", "user": "1", "sendtime": "2019-01-29 12:16:54"}, "profile": {"jsonns": "profile/vehicle", "item": {"Latitude": 121.3808528, "NS_Indicator": " ", "Longitude": 31.34319444, "EW_Indicator": " ", "Speed": 0, "Course": 70.94, "MSL_Altitude": 0}}}}}}
