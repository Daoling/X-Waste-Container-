# -*- coding: UTF-8 -*-
from django.db import models


# 管理员表
class User(models.Model):
    userName = models.CharField(max_length=20)
    password= models.CharField(max_length=20)
    remarks = models.CharField(max_length=100)

class  UserModels(models.Model):

    userName = models.CharField(max_length=20)
    password= models.CharField(max_length=20)

    userName = models.CharField(max_length=100)
    openId = models.CharField(max_length=100)
    userType = models.CharField(max_length=100)
    userTypeName = models.CharField(max_length=100)

    isbinding = models.CharField(max_length=5)
    isbindingdevice = models.CharField(max_length=20)
    # add user info
    nickname = models.CharField(max_length=100)  # 微信昵称
    sex = models.CharField(max_length=3)  # 性别
    language = models.CharField(max_length=20)  # 语言
    city = models.CharField(max_length=50)  # 城市
    province = models.CharField(max_length=50)  # 省
    country = models.CharField(max_length=50)  # 国家
    headimgurl = models.CharField(max_length=200)  # 头像
    subscribe_scene = models.CharField(max_length=50)  # 返回用户关注的渠道来源，ADD_SCENE_SEARCH 公众号搜索，
    # ADD_SCENE_ACCOUNT_MIGRATION 公众号迁移，ADD_SCENE_PROFILE_CARD 名片分享，ADD_SCENE_QR_CODE 扫描二维码，
    # ADD_SCENEPROFILE LINK 图文页内名称点击，ADD_SCENE_PROFILE_ITEM 图文页右上角菜单，ADD_SCENE_PAID 支付后关注，
    # ADD_SCENE_OTHERS 其他


    createdDateTime = models.DateTimeField("created date")
    updateTime = models.DateTimeField("created date")
    remarks = models.CharField(max_length=100)


class  TrashModels(models.Model):

    deviceName = models.CharField(max_length=50)  # devicename
    deviceId = models.CharField(max_length=50)  # deviceId
    devicepassword = models.CharField(max_length=50)
    deviceType = models.CharField(max_length=50)

    city = models.CharField(max_length=30)  # 城市
    province = models.CharField(max_length=20)  # 省
    address = models.CharField(max_length=50)  # 城市
    longitude = models.CharField(max_length=20)  # 经度
    dimension = models.CharField(max_length=20)  # 维度
    status = models.CharField(max_length=3)  # 1 可用 0 不可用
    lineStatus = models.CharField(max_length=3)  # 1 在线 0 不在线

    onTime = models.DateTimeField("created date")  # 上线时间
    offTime = models.DateTimeField("created date") # 下线时间



    createdDateTime = models.DateTimeField("created date")
    updateTime = models.DateTimeField("created date")
    remarks = models.CharField(max_length=100)

class TrashStatusModels(models.Model):  # 垃圾桶状态表

    deviceId = models.CharField(max_length=50)  # deviceId
    statusType = models.CharField(max_length=3)  # 类别  各个桶数据
    typeName = models.CharField(max_length=50)  # 类别名称
    value = models.CharField(max_length=50) #



class QRcodeModels(models.Model): # 二维码管理表

    qrid = models.CharField(max_length=50)  # deviceId
    type  = models.CharField(max_length=3) # 种类 1 积分二维码  2

    imageUrl = models.CharField(max_length=50)# 图片位置
    imageContext= models.CharField(max_length=30)# 图片位置
    value = models.CharField(max_length=50)#





