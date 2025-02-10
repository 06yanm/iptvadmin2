from django.db import models
from deviceAdmin.models import Device

# Create your models here.
# 分类
class Category(models.Model):
    objects = models.Manager()
    # 分类名
    name = models.CharField(max_length=100)
    # 简介
    desc = models.CharField(max_length=255, blank=True, default='')
    # 所属设备
    devices = models.ManyToManyField(Device, related_name="canSee")


# 频道
class Channel(models.Model):
    objects = models.Manager()
    # 频道名
    name = models.CharField(max_length=100)
    # 频道视频链接
    url = models.CharField(max_length=255)
    # 简介
    desc = models.CharField(max_length=255, blank=True, default='')
    # 在分类中隐藏
    hidden = models.BooleanField(default=False)
    # 所属分类
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="channels")