from django.db import models


# Create your models here.
class BasicSetting(models.Model):
    # 方便pycharm提示
    objects = models.Manager()
    # 数据id
    id = models.AutoField(primary_key=True)
    # 广告内容
    adtext = models.CharField(max_length=100, default="这是广告位置, 10秒后消失")
    # 广告显示时间
    showTime = models.IntegerField(default=10)
    # 软件启动图片
    imgStart = models.CharField(max_length=100, default="")
    # 软件退出图片
    imgEnd = models.CharField(max_length=100, default="")
    # 全局epg配置地址
    epgUrl = models.CharField(max_length=100, default="")
    # 全局User-Agent
    ua = models.CharField(max_length=100, default="SYTV/1.6")
    # 总启动次数
    startCount = models.IntegerField(default=0)


class StartCountDate(models.Model):
    objects = models.Manager()
    # 日期
    date = models.CharField(max_length=20)
    # 启动次数
    count = models.IntegerField(default=0)