import datetime
import os
from django.http import Http404
from django.shortcuts import HttpResponse, render
from adminApi import settings
from .models import BasicSetting, StartCountDate
from deviceAdmin.models import Device
from softAdmin.models import Channel, Category
import json
import time
import hashlib
import gzip
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii

# 当日的启动次数+1
def addStartCount(date):
    d = StartCountDate.objects.filter(date=date)
    if d:
        d = d.first()
        d.count += 1
        d.save()
    else:
        d = StartCountDate(date=date, count=1)
        d.save()


# 根据日期获取启动次数
def getStartCountByDate(date):
    try:
        data = StartCountDate.objects.filter(date=date)
        data = data.first().count
    except Exception as e:
        return 0
    return data

# 获取启动次数
def getStartCount():
    data = BasicSetting.objects.first()
    return data.startCount

# 在软件启动时获取配置信息
def getinfo(request):
    data = BasicSetting.objects.first()
    data = {
        "adtext": data.adtext,
        "showtime": data.showTime,
        "imgstart": data.imgStart,
        "imgend": data.imgEnd,
        "epgurl": data.epgUrl,
        "tmua": data.ua
    }
    if request.method == 'GET':
        response = HttpResponse(gzip.compress(json.dumps(data).encode('utf-8')))
        response['Content-Encoding'] = 'gzip'
        response['Content-Type'] = 'text/html; charset=utf-8'
        response['Vary'] = 'Accept-Encoding'
        return response
    elif request.method == 'POST':
        deviceInfo = request.POST.get('deviceInfo')
        if not deviceInfo:
            response = HttpResponse(gzip.compress(json.dumps(data).encode('utf-8')))
            response['Content-Encoding'] = 'gzip'
            response['Content-Type'] = 'text/html; charset=utf-8'
            response['Vary'] = 'Accept-Encoding'
            return response
        deviceInfo = json.loads(deviceInfo)
        device = Device.objects.filter(macAddress=deviceInfo['mac'])
        s = BasicSetting.objects.first()
        s.startCount += 1
        addStartCount(datetime.datetime.now().date().strftime("%Y-%m-%d"))
        s.save()
        if device.exists():
            device = device.first()
            device.startCount += 1
            device.save()
            response = HttpResponse(gzip.compress(json.dumps(data).encode('utf-8')))
            response['Content-Encoding'] = 'gzip'
            response['Content-Type'] = 'text/html; charset=utf-8'
            response['Vary'] = 'Accept-Encoding'
            return response
        else:
            device = Device.objects.create(
                macAddress = deviceInfo['mac'],
                androidId = deviceInfo['androidid'],
                deviceName = deviceInfo['model'],
                ipAddress = request.META.get('REMOTE_ADDR').split(',')[0],
                isAuthorized = False,
                startCount = 1
            )
            device.save()
            response = HttpResponse(gzip.compress(json.dumps(data).encode('utf-8')))
            response['Content-Encoding'] = 'gzip'
            response['Content-Type'] = 'text/html; charset=utf-8'
            response['Vary'] = 'Accept-Encoding'
            return response

# 进行AES加密
def aes_encrypt(data, secret_key):
    secret_key = secret_key[:16]  # 确保密钥长度为16字节
    cipher = AES.new(secret_key.encode(), AES.MODE_ECB)
    padded_data = pad(data.encode(), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return encrypted_data


# md5hash散列
def md5_hash(plain_text):
    md5 = hashlib.md5()
    md5.update(plain_text.encode('utf-8'))
    return md5.hexdigest()


def getMiniData():
    miniData = ""
    allCates = Category.objects.all()
    for cate in allCates:
        cateName = cate.name
        miniData = miniData + cateName + ",#genre#\r\n"
        channelsSet = Channel.objects.filter(category=cate, hidden=False)
        for channel in channelsSet:
            channelName = channel.name
            channelUrl = channel.url
            miniData = miniData + channelName + "," + channelUrl + "\r\n"
    print(miniData)
    return miniData



# 获取直播源数据
def getlive(request):
    if request.method == 'GET':
        return HttpResponse("")
    elif request.method == 'POST':
        ttime = int(time.time())
        # print(ttime)
        key = md5_hash(str(ttime)+"AD80F93B542B"+"8b14ecf6ae028f9b6d25fa547eabad85")
        ke = key[13:]
        # print("key:"+ke)
        f = aes_encrypt(getMiniData(), ke)
        rawData = binascii.hexlify(f)
        response = HttpResponse(gzip.compress(ke.encode("utf-8")+rawData))
        response['Content-Encoding'] = 'gzip'
        response['Content-Type'] = 'text/html; charset=utf-8'
        response['Vary'] = 'Accept-Encoding'
        return response


# 获取台标
def getlogo(request, name):
    # 返回static图片资源
    image_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'tv')
    image_path = os.path.join(image_dir, name)
    if not os.path.exists(image_path):
        raise Http404("Image does not exist")
    with open(image_path, 'rb') as f:
        return HttpResponse(f.read(), content_type='image/png')
