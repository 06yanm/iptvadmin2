import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Device
from utils import need_login, api_need_login

# 全局每页数据数量
LIMIT = 10

# 获取设备总数
def getDeviceNum():
    num = Device.objects.count()
    return num

# 获取设备总页数
@api_need_login
def getDevicePageNum(request):
    if request.method == 'GET':
        num = getDeviceByPageMethod(1)[1]
        return JsonResponse({"code": 200, "data": num})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误"})


# 批量修改设备可看分类
@api_need_login
def changeCateMany(request):
    if request.method == 'POST':
        ids = json.loads(request.POST.get('cateIds'))
        devices = json.loads(request.POST.get('device'))
        if devices == [] or not devices:
            return JsonResponse({"code": 400, "msg": "未选择设备！"})
        if ids == [] or not ids:
            for device in devices:
                device = Device.objects.get(id=device)
                device.canSee.clear()
                device.save()
            return JsonResponse({"code": 200, "msg": "清空设备分类成功"})
        for device in devices:
            device = Device.objects.get(id=device)
            device.canSee.clear()
            device.canSee.set(ids)
            device.save()
        return JsonResponse({"code": 200, "msg": "修改分类成功"})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误"})


# 根据页码获取设备列表(方法)
def getDeviceByPageMethod(page):
    devices = Device.objects.all().order_by('-id')
    paginator = Paginator(devices, LIMIT)
    try:
        devices = paginator.page(page)
    except PageNotAnInteger:
        devices = paginator.page(1)
    except EmptyPage:
        devices = paginator.page(paginator.num_pages)
    deviceList = []
    num = (int(page) - 1) * LIMIT
    for device in devices:
        num += 1
        canSee = ",".join(str(value.name) for value in device.canSee.all())
        if canSee == "":
            canSee = "无"
        deviceList.append({
            "num": num,
            "id": device.id,
            "deviceName": device.deviceName,
            "mac": device.macAddress,
            "androidId": device.androidId,
            "isAuth": device.isAuthorized,
            "canSee": canSee,
            "startCount": device.startCount,
            "ip": device.ipAddress,
            "lastTime": device.lastOnlineTime
        })
    return deviceList, paginator.num_pages


# 根据页码获取设备列表(接口)
@api_need_login
def getDeviceByPage(request):
    if request.method == 'GET':
        page = request.GET.get('page', '1')
        deviceList = getDeviceByPageMethod(page)
        return JsonResponse({"code": 200, "msg": "获取成功", "data": deviceList[0]})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误"})

# 根据id列表批量授权
@api_need_login
def authByIds(request):
    if request.method == 'POST':
        ids = json.loads(request.POST.get('ids'))
        if ids and ids != []:
            num = 0
            for id in ids:
                try:
                    device = Device.objects.get(id=id)
                    device.isAuthorized = True
                    device.save()
                    num += 1
                except Device.DoesNotExist:
                    continue
            return JsonResponse({"code": 200, "msg": f"批量授权成功{num}个设备！"})
        else:
            return JsonResponse({"code": 400, "msg": "未选择数据！"})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误"})


# 根据id列表批量解除授权
@api_need_login
def unAuthByIds(request):
    if request.method == 'POST':
        ids = json.loads(request.POST.get('ids'))
        if ids and ids != []:
            num = 0
            for id in ids:
                try:
                    device = Device.objects.get(id=id)
                    device.isAuthorized = False
                    device.save()
                    num += 1
                except Device.DoesNotExist:
                    continue
            return JsonResponse({"code": 200, "msg": f"批量解除授权成功{num}个设备！"})
        else:
            return JsonResponse({"code": 400, "msg": "未选择数据！"})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误"})