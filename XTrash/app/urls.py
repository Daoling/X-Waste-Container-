
from django.conf.urls import url
from django.contrib import admin

from app import views

urlpatterns = [
    url(r'^$',		    views.home),
    url(r'^upload/',    views.upload),

    # 微信小程序
    url(r'^getqr/', views.getQrImage),  # 获取 二维码
    url(r'^openforqr/', views.openForQR),  # 扫二维码


    # 垃圾箱

    url(r'^get_qrContent/', views.getQrContentTrash),  # 获取 二维码内容
    url(r'^add_operationecord/', views.addOperationRecordTrash),  # 用户操作记录
    url(r'^upload_picture/', views.uploadPictureTrash),  # 拍照上传接口
    url(r'^upload_weight/', views.uploadWeightTrash),  # 称重 接口 参数 种类。json  返回 成功
    url(r'^upload_height/', views.uploadHeightTrash),  # 测量高度
    url(r'^getCost/', views.getCostTrash),  # 本次操作 所有信息




]

