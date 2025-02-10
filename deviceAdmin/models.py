from django.db import models

# 设备表
class Device(models.Model):
    objects = models.Manager()
    # 设备mac地址: 00:0c:29:3d:7f:9a
    macAddress = models.CharField(max_length=17)
    # 设备id(AndroidId): e3f6e8d0a6a5e4f5
    androidId = models.CharField(max_length=64)
    # 设备编号名称: 21091116AC
    deviceName = models.CharField(max_length=64)
    # 设备ip地址: 192.168.1.1
    ipAddress = models.GenericIPAddressField()
    # 设备ip地区: 河北石家庄 电信
    ipArea = models.CharField(max_length=64)
    # 设备最后一次上线时间: 2021-09-11 16:00:00
    lastOnlineTime = models.DateTimeField(auto_now=True)
    # 是否授权
    isAuthorized = models.BooleanField(default=False)
    # 启动次数
    startCount = models.IntegerField(default=0)
