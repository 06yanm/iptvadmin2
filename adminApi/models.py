from django.db import models

class AdminInfo(models.Model):
    objects = models.Manager()
    # 账号
    username = models.CharField(max_length=20, unique=True)
    # 昵称
    nickname = models.CharField(max_length=20, unique=True)
    # 密码
    password = models.CharField(max_length=20)
    # 头像
    avatar = models.CharField(max_length=255, default="")



