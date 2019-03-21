# -*- coding: UTF-8 -*-
import paho.mqtt.publish as publish
import time
import paho.mqtt.client as mqtt
import requests.packages.urllib3.util.ssl_
import json

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

HOST = "118.24.129.102"
PORT = 1883

HOST = "www.yikeni.com"
PORT = 1883

# HOST = "13.229.7.162"
# PORT = 1888

# HOST = '192.144.139.54'
# PORT = 1883

# HOST = "118.24.129.102"
# PORT = 1888

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("xtrash/0001")

def on_message(client, userdata, msg):
    print(msg.topic+" "+msg.payload.decode("utf-8"))

if __name__ == '__main__':
    client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    client = mqtt.Client(client_id)    # ClientId不能重复，所以使用当前时间



    client.username_pw_set("secomiot", "#secom&2019@")  # 必须设置，否则会返回「Connected with result code 4」

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT, 60)



   # client.publish("v1/mobile/telemetry", "jsonStr", qos=0, retain=False)  # 发布消息

    #publish.single("iot", "你好 MQTT", qos = 1,hostname=HOST,port=PORT, client_id=client_id,auth = {'username':"secomiot", 'password':"#secom&2019@"})

    client.loop_start()



    print('Interval 1')

    for i in range(300):
       # print('Interval ' + str(i))
        # client.subscribe('lettuce')  #client1 subcribes a topic 'manipulated'



       # client.publish("v1/mobile/telemetry", '===>')  # client2 publishes topic 'manipulated' with content 'i*0.02'

        time.sleep(3)

    client.loop_stop()