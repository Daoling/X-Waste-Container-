# coding:utf-8
from PyQt5 import QtCore,QtGui,QtWidgets
import sys
import qtawesome
import serial
import json
import requests
import createImage
import datetime
import paho.mqtt.publish as publish
import time
import paho.mqtt.client as mqtt
import requests.packages.urllib3.util.ssl_

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

global LOGIN_SIGN
global USER_ID
global TOKEN
global USER_NAME
LOGIN_SIGN = False
USER_ID = ""
TOKEN = ""
USER_NAME = ""
DeviceId = "001"
HOST = "www.yikeni.com"
PORT = 1883
ser=serial.Serial("/dev/ttyUSB0",115200,timeout=0.5)

class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.use_palette()

    def init_ui(self):
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格

        #self.main_layout.addWidget(self.left_widget,0,0,12,2) # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget,0,0,12,12) # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget) # 设置窗口主部件

        self.right_bar_widget = QtWidgets.QWidget() # 右侧顶部搜索框部件
        self.right_bar_layout = QtWidgets.QGridLayout() # 右侧顶部搜索框网格布局
        self.right_bar_widget.setLayout(self.right_bar_layout)

        self.right_recommend_label = QtWidgets.QLabel(self)
        jpg = QtGui.QPixmap('title.jpg')
        self.right_recommend_label.setPixmap(jpg)
        self.right_recommend_label.setAlignment(QtCore.Qt.AlignCenter)

        self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)

        self.right_recommend_widget = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)

        self.recommend_button_1 = QtWidgets.QToolButton()
        self.recommend_button_1.setText("视频介绍") # 设置按钮文本
        self.recommend_button_1.setIcon(QtGui.QIcon('1.jpg')) # 设置按钮图标
        self.recommend_button_1.setIconSize(QtCore.QSize(300,300)) # 设置图标大小
        self.recommend_button_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文

        self.recommend_button_2 = QtWidgets.QToolButton()
        self.recommend_button_2.setText("垃圾回收")
        self.recommend_button_2.setIcon(QtGui.QIcon('2.jpg'))
        self.recommend_button_2.setIconSize(QtCore.QSize(300, 300))
        self.recommend_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_3 = QtWidgets.QToolButton()
        self.recommend_button_3.setText("关于我们")
        self.recommend_button_3.setIcon(QtGui.QIcon('3.jpg'))
        self.recommend_button_3.setIconSize(QtCore.QSize(300, 300))
        self.recommend_button_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.right_recommend_layout.addWidget(self.recommend_button_1,0,0)
        self.right_recommend_layout.addWidget(self.recommend_button_2,0,1)
        self.right_recommend_layout.addWidget(self.recommend_button_3, 0, 2)

       # self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)
        self.right_layout.addWidget(self.right_recommend_widget, 2, 0, 2, 9)

        self.recommend_button_2.clicked.connect(self.showLoginDialog)


        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')

        self.right_recommend_widget.setStyleSheet(
            '''
                QToolButton{border:none;}
                QToolButton:hover{border-bottom:2px solid #F76677;}
            ''')

    def showLoginDialog(self):
        self.dialog = Login()
        self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)  # 该模式下，只有该dialog关闭，才可以关闭父界面
        self.dialog.show()
        self.dialog.exec_()
        if LOGIN_SIGN:
            #print( self.dialog.exec_())
            self.shwoDeliverDialog()

    def shwoDeliverDialog(self):
        self.Deliverdialog = Deliver()
        self.Deliverdialog.token = TOKEN
        self.Deliverdialog.userId = USER_ID
        self.Deliverdialog.setWindowModality(QtCore.Qt.ApplicationModal)  # 该模式下，只有该dialog关闭，才可以关闭父界面
        self.Deliverdialog.showMaximized()


    def use_palette(self):
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('backgroud.jpg')))
        self.setPalette(window_pale)

    def login(self):
        pass


class Login(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.use_palette()
        self.token = ""
        self.qrid = ""
        self.userId = ""
        self.userName = ""
        self.set_input()
        self.init_ui()
        self.client = ""
        self.init_mqtt()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("xtrash")

    def on_message(self, client, userdata, msg):
        global USER_ID
        global USER_NAME
        global TOKEN
        print(msg.topic + " " + msg.payload.decode("utf-8"))
        mqtt_message = msg.payload
        if msg.topic == 'data_msg':
            jsonData = json.loads(mqtt_message)
            TOKEN = jsonData["token"]
            USER_NAME = jsonData["usrname"]
            USER_ID =  jsonData["usrid"]
            self.btnOK()


    def init_mqtt(self):
        client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        client = mqtt.Client(client_id)  # ClientId不能重复，所以使用当前时间

        client.username_pw_set("secomiot", "#secom&2019@")  # 必须设置，否则会返回「Connected with result code 4」

        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(HOST, PORT, 60)

        client.loop_start()

    def set_input(self):
        global USER_ID
        global USER_NAME
        global TOKEN
        TOKEN = ""
        USER_NAME = ""
        USER_ID = ""
        url = "https://www.yikeni.com/xtrash/get_qrContent"
        response = requests.get(url, headers={'deviceId': DeviceId})
        info_dict = json.loads(response.text)
        self.token = info_dict["token"]
        self.qrid = info_dict["qrid"]
        createImage.CreateImage.getQrPath(self.qrid)


    def init_ui(self):
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格

        #self.main_layout.addWidget(self.left_widget,0,0,12,2) # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget,0,0,12,12) # 右侧部件在第0行第3列，占8行9列

        self.right_recommend_label = QtWidgets.QLabel(self)
        self.right_recommend_label.setText("")
        self.right_recommend_label.setStyleSheet(
            "font:60pt '楷体';color:red")
        self.right_recommend_label.setAlignment(QtCore.Qt.AlignTop| QtCore.Qt.AlignRight)

        self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)

        self.right_recommend_widget = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)

        self.recommend_button = QtWidgets.QToolButton()
        self.recommend_button.setText("login")  # 设置按钮文本
        self.recommend_button.setIcon(QtGui.QIcon('login.png'))  # 设置按钮图标
        self.recommend_button.setIconSize(QtCore.QSize(300, 300))  # 设置图标大小
        self.recommend_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)  # 设置按钮形式为上图下文
        self.recommend_button.clicked.connect(self.btnOK)


        self.right_recommend_layout.addWidget(self.recommend_button,0,1)

       # self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)
        self.right_layout.addWidget(self.right_recommend_widget, 3, 0, 2, 9)

        #self.recommend_button.accepted.connect(self.accept)

        self.btn_1 = QtWidgets.QPushButton("取消登录")
        self.btn_1.clicked.connect(self.btnCancel)

        self.right_layout.addWidget(self.btn_1, 4, 0, 1, 9)
        self.timer = QtCore.QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.Cancel)  # 计时结束调用operate()方法
        self.timer.start(1000)  # 设置计时间隔并启动

        self.setLayout(self.main_layout)


        self.right_widget.setStyleSheet('''
                    QWidget#right_widget{
                        color:#232C51;
                        background:white;
                        border-top:1px solid darkGray;
                        border-bottom:1px solid darkGray;
                        border-right:1px solid darkGray;
                        border-top-right-radius:10px;
                        border-bottom-right-radius:10px;
                    }
                    QLabel#right_lable{
                        border:none;
                        font-size:16px;
                        font-weight:700;
                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                    }
                ''')

    def use_palette(self):
        self.setWindowTitle("扫码登录")
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('backgroud.jpg')))
        self.setPalette(window_pale)

    def Cancel(self):
        str_second = self.right_recommend_label.text().strip("秒")
        try:
            second = int(str_second)
        except:
            second = 60
        second = second - 1
        if second == 0:
            self.btnCancel()
        self.right_recommend_label.setText(str(second) + "秒")


    def btnCancel(self):
        global LOGIN_SIGN
        LOGIN_SIGN = False

        print (LOGIN_SIGN)
        self.right_recommend_label.setText("")
        self.timer.stop()
        self.client.loop_stop()
        self.close()

    def btnOK(self):
        global LOGIN_SIGN
        LOGIN_SIGN = True
        print (LOGIN_SIGN)
        self.right_recommend_label.setText("")
        self.timer.stop()
        self.client.loop_stop()
        self.close()



class Deliver(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.use_palette()
        self.userId = ""
        self.token = ""

    def init_ui(self):
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格

        #self.main_layout.addWidget(self.left_widget,0,0,12,2) # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget,0,0,12,12) # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget) # 设置窗口主部件

        self.right_recommend_widget = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)

        self.recommend_button_1 = QtWidgets.QToolButton()
        #self.recommend_button_1.setText("硬板纸") # 设置按钮文本
        self.recommend_button_1.setIcon(QtGui.QIcon('01.jpg')) # 设置按钮图标
        self.recommend_button_1.setIconSize(QtCore.QSize(300,300)) # 设置图标大小
        self.recommend_button_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
        self.recommend_button_1.clicked.connect(self.openDoor)

        self.recommend_button_2 = QtWidgets.QToolButton()
        #self.recommend_button_2.setText("所料制品")
        self.recommend_button_2.setIcon(QtGui.QIcon('02.jpg'))
        self.recommend_button_2.setIconSize(QtCore.QSize(300, 300))
        self.recommend_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.recommend_button_2.clicked.connect(self.openDoor)

        self.recommend_button_3 = QtWidgets.QToolButton()
        #self.recommend_button_3.setText("金属类")
        self.recommend_button_3.setIcon(QtGui.QIcon('03.jpg'))
        self.recommend_button_3.setIconSize(QtCore.QSize(300, 300))
        self.recommend_button_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.recommend_button_3.clicked.connect(self.openDoor)


        self.recommend_button_4 = QtWidgets.QToolButton()
        #self.recommend_button_4.setText("玻璃")
        self.recommend_button_4.setIcon(QtGui.QIcon('04.jpg'))
        self.recommend_button_4.setIconSize(QtCore.QSize(300, 300))
        self.recommend_button_4.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.recommend_button_4.clicked.connect(self.openDoor)

        self.right_recommend_layout.addWidget(self.recommend_button_1,0,0)
        self.right_recommend_layout.addWidget(self.recommend_button_2,0,1)
        self.right_recommend_layout.addWidget(self.recommend_button_3, 0, 2)
        self.right_recommend_layout.addWidget(self.recommend_button_4, 0, 3)

        self.recommend_button_5 = QtWidgets.QToolButton()
        #self.recommend_button_5.setText("有害类") # 设置按钮文本
        self.recommend_button_5.setIcon(QtGui.QIcon('05.jpg')) # 设置按钮图标
        self.recommend_button_5.setIconSize(QtCore.QSize(300,300)) # 设置图标大小
        self.recommend_button_5.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
        self.recommend_button_5.clicked.connect(self.openDoor)

        self.recommend_button_6 = QtWidgets.QToolButton()
        #self.recommend_button_6.setText("")
        self.recommend_button_6.setIcon(QtGui.QIcon('06.jpg'))
        self.recommend_button_6.setIconSize(QtCore.QSize(300, 300))
        self.recommend_button_6.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.recommend_button_6.clicked.connect(self.openDoor)

        self.recommend_button_7 = QtWidgets.QToolButton()
        #self.recommend_button_7.setText("其他")
        self.recommend_button_7.setIcon(QtGui.QIcon('07.jpg'))
        self.recommend_button_7.setIconSize(QtCore.QSize(300, 300))
        self.recommend_button_7.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.recommend_button_7.clicked.connect(self.openDoor)

        self.recommend_button_8 = QtWidgets.QToolButton()
        #self.recommend_button_8.setText("退出")
        self.recommend_button_8.setIcon(QtGui.QIcon('08.jpg'))
        self.recommend_button_8.setIconSize(QtCore.QSize(300, 300))
        self.recommend_button_8.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.recommend_button_8.clicked.connect(self.exit)


        self.right_recommend_layout.addWidget(self.recommend_button_5, 1, 0)
        self.right_recommend_layout.addWidget(self.recommend_button_6, 1, 1)
        self.right_recommend_layout.addWidget(self.recommend_button_7, 1, 2)
        self.right_recommend_layout.addWidget(self.recommend_button_8, 1, 3)

        self.right_layout.addWidget(self.right_recommend_widget, 1, 0, 2, 9)

        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')

        self.right_recommend_widget.setStyleSheet(
            '''
                QToolButton{border:none;}
                QToolButton:hover{border-bottom:2px solid #F76677;}
            ''')

        self.setLayout(self.main_layout)

    def use_palette(self):
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('backgroud.jpg')))
        self.setPalette(window_pale)

    def exit(self):
        self.close()

    def openDoor(self):
        DoorNO = ""
        if self.sender() == self.recommend_button_1:
            DoorNO = "01"
        if self.sender() == self.recommend_button_2:
            DoorNO = "02"
        if self.sender() == self.recommend_button_3:
            DoorNO = "03"
        if self.sender() == self.recommend_button_4:
            DoorNO = "04"
        if self.sender() == self.recommend_button_5:
            DoorNO = "05"
        if self.sender() == self.recommend_button_6:
            DoorNO = "06"
        if self.sender() == self.recommend_button_7:
            DoorNO = "07"
        self.Opendailog = Door()
        self.Opendailog.token = self.token
        self.Opendailog.userId = self.userId
        self.Opendailog.DoorNO = DoorNO
        self.Opendailog.setWindowModality(QtCore.Qt.ApplicationModal)  # 该模式下，只有该dialog关闭，才可以关闭父界面
        self.Opendailog.show()
        self.Opendailog.exec_()


class Door(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.use_palette()
        self.init_ui()
        self.result = False
        self.OpenDoor()
        self.userId = ""
        self.token = ""
        self.DoorNO = ""

    def init_ui(self):
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格

        #self.main_layout.addWidget(self.left_widget,0,0,12,2) # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget,0,0,12,12) # 右侧部件在第0行第3列，占8行9列

        self.right_recommend_label = QtWidgets.QLabel(self)
        self.right_recommend_label.setText("60秒后关闭仓门")
        self.right_recommend_label.setStyleSheet(
            "font:60pt '楷体';color:red")
        self.right_recommend_label.setAlignment(QtCore.Qt.AlignTop| QtCore.Qt.AlignRight)

        self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)

        self.right_recommend_widget = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)

        self.recommend_button = QtWidgets.QToolButton()
        self.recommend_button.setText("关闭仓门")  # 设置按钮文本
        self.recommend_button.setIcon(QtGui.QIcon('cloedDoor.jpg'))  # 设置按钮图标
        self.recommend_button.setIconSize(QtCore.QSize(200, 200))  # 设置图标大小
        self.recommend_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)  # 设置按钮形式为上图下文
        self.recommend_button.clicked.connect(self.btnOK)

        self.right_recommend_layout.addWidget(self.recommend_button,0,1)

       # self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)
        self.right_layout.addWidget(self.right_recommend_widget, 3, 0, 2, 9)

        #self.recommend_button.accepted.connect(self.accept)

        self.timer = QtCore.QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.Cancel)  # 计时结束调用operate()方法
        self.timer.start(1000)  # 设置计时间隔并启动

        self.setLayout(self.main_layout)


        self.right_widget.setStyleSheet('''
                    QWidget#right_widget{
                        color:#232C51;
                        background:white;
                        border-top:1px solid darkGray;
                        border-bottom:1px solid darkGray;
                        border-right:1px solid darkGray;
                        border-top-right-radius:10px;
                        border-bottom-right-radius:10px;
                    }
                    QLabel#right_lable{
                        border:none;
                        font-size:16px;
                        font-weight:700;
                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                    }
                ''')

    def use_palette(self):
        self.setWindowTitle("扫码登录")
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('backgroud.jpg')))
        self.setPalette(window_pale)

    def OpenDoor(self, Number):
        input_dict = "{‘Action’:’OpenDoor’,’Number’:Number}"
        input_str = json.dumps(input_dict)
        ser.write(input_str)
        length = ser.inWaiting()
        res = ser.read(length)
        out_put = json.loads(res)
        if out_put["info"] == "OK":
            self.record_action("1")
        else:
            self.record_action("1") #记录开门失败，告警


    def Cancel(self):
        str_second = self.right_recommend_label.text().strip("秒")
        try:
            second = int(str_second)
        except:
            second = 60
        second = second - 1
        if second == 0:
            self.btnCancel()
        self.right_recommend_label.setText(str(second) + "秒")


    def btnCancel(self):
        """超时关门"""
        global LOGIN_SIGN
        LOGIN_SIGN = False
        self.right_recommend_label.setText("60秒后关闭仓门")
        self.timer.stop()
        res  = self.do_action("CloseDoor")
        if res:
            photo = self.do_action("Photograph")
            Weigh = self.do_action("Weigh")
            Height = self.do_action("Height")
        self.close()

    def btnOK(self):
        """手动关门"""
        global LOGIN_SIGN
        LOGIN_SIGN = True

        self.right_recommend_label.setText("60秒后关闭仓门")
        self.timer.stop()
        res = self.do_action("CloseDoor")
        if res:
            photo = self.do_action("Photograph")
            self.upload_picture(photo)
            Weigh = self.do_action("Weigh")
            self.upload_weigh(Weigh)
            Height = self.do_action("Height")
            self.upload_Height(Height)
        self.close()

    def upload_picture(self, picture):
        url = "https://www.yikeni.com/xtrash/upload_picture"
        header_dict = {"deviceId":DeviceId,
                     "token":self.token,
                     "type":"1",
                    'Api-Key':'InhpeWFuZzA4MDdJBtx4AWlPpI_Oxx1Ki8',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
                    }

        time_string = datetime.datetime.now().strftime("%Y-%m-%d_%H:%S:%M")

        picture_name = DeviceId + "_" + time_string + ".png"
        multiple_files = [
            ('images', (picture_name, picture, 'image/png'))
        ]
        response = requests.post(url, files=multiple_files, headers=header_dict)
        print(response.text)

    def upload_weigh(self, Weigh):
        url = "https://www.yikeni.com/xtrash/upload_weight"
        header_dict = {"deviceId": DeviceId,
                       "weight":Weigh,
                       "token": self.token,
                       "userId": self.userId
                       }
        response = requests.get(url, header_dict)
        print(response.text)

    def upload_Height(self, Height):
        url = "https://www.yikeni.com/xtrash/upload_height"
        header_dict = {"deviceId": DeviceId,
                       "height": Height,
                       "token": self.token,
                       "userId": self.userId
                       }
        response = requests.get(url, header_dict)
        print(response.text)


    def record_action(self,Type):
        """ Type 操作类型  1：开门  2：关门"""
        url = "https://www.yikeni.com/xtrash/add_operationecord/"
        body_json = {"type":Type, "userId":self.userId, "token": self.token}
        response = requests.get(url, body_json)

        print(response.text)

    def do_action(self, action):
        input_dict = {"Action":action,"Number":self.DoorNO}
        input_str = json.dumps(input_dict)
        ser.write(input_str)
        length = ser.inWaiting()
        res = ser.read(length)
        out_put = json.loads(res)
        return out_put["info"]



def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()

    gui.showFullScreen()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()