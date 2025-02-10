from django.template import loader
from django.shortcuts import render
from django.urls import reverse
from android.models import BasicSetting
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import AdminInfo
from deviceAdmin.views import getDeviceByPageMethod
from softAdmin.views import getAllCategory
from softAdmin.views import getCategoriesByPageMethod
from softAdmin.views import getChannelsByPageMethod
from deviceAdmin.views import getDeviceNum
from softAdmin.views import getCategoryCount, getChannelCount
from android.views import getStartCount
from datetime import datetime, timedelta
from android.views import getStartCountByDate
from utils import need_login, api_need_login


def notFound(request, exception=""):
    return render(request, 'error.html')


def logout(request):
    if 'logged_in' in request.session:
        del request.session['logged_in']
    return HttpResponseRedirect(reverse('login'))

# 修改账号密码
@api_need_login
def changePassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        nickname = request.POST.get('nickname')
        avatar = request.POST.get('avatar')
        d = AdminInfo.objects.first()
        if d:
            if username: d.username = username
            if password: d.password = password
            if nickname: d.nickname = nickname
            if avatar: d.avatar = avatar
            d.save()
            return JsonResponse({"code": "200", "msg": "修改成功"})
        else:
            return JsonResponse({"code": "400", "msg": "修改失败: 账号不存在"})
    else:
        return JsonResponse({"code": "401", "msg": "请求方式错误"})


# 后台登陆
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        d = AdminInfo.objects.filter(username=username).first()
        if d:
            if d.password == password:
                request.session['logged_in'] = True
                return JsonResponse({"code": "200", "msg": "登陆成功", "redirect": "/admin/main"})
            else:
                return JsonResponse({"code": "400", "msg": "登陆失败: 账号或密码错误", "redirect": ""})
        else:
            return JsonResponse({"code": "401", "msg": "登陆失败: 账号不存在", "redirect": ""})

    else:
        return render(request, 'login.html')

# 获取图表展示信息
def getCharts():
    charts = []
    current = datetime.now().date()
    for i in range(7):
        charts.append([
            (current - timedelta(days=i)).strftime("%m-%d"),
            getStartCountByDate((current - timedelta(days=i)).strftime("%Y-%m-%d"))
        ])
    return charts


@need_login
# 后台首页
def mainPage(request):
    content = {
        "title": "后台首页",
        "startCount": getStartCount(),
        "deviceCount": getDeviceNum(),
        "cateCount": getCategoryCount(),
        "channelCount": getChannelCount(),
        "charts": getCharts()
    }
    return render(request, 'index.html', content)


# 设备管理
@need_login
def devicePage(request):
    d, b = getDeviceByPageMethod(1)
    cates = getAllCategory()
    content = {
        "title": "设备管理",
        "allPages": b,
        "cates": cates,
    }
    return render(request, 'device.html', content)

# epg设置
@need_login
def epgPage(request):
    setting = BasicSetting.objects.first()
    content = {
        "title": "EPG设置",
        "epg": setting.epgUrl,
    }
    return render(request, 'epg.html', content)

# 分类管理
@need_login
def categoryPage(request):
    content = {
        "title": "分类管理",
        "allPages": getCategoriesByPageMethod(1)[1]
    }
    return render(request, 'category.html', content)

# 频道管理
@need_login
def channelPage(request):
    content = {
        "title": "频道管理",
        "allPages": getChannelsByPageMethod(1)[1],
        "cates": getAllCategory()
    }
    return render(request, 'channel.html', content)

# 软件公告
@need_login
def announcementPage(request):
    setting = BasicSetting.objects.first()
    content = {
        "title": "软件公告",
        "content": setting.adtext,
        "showtime": setting.showTime
    }
    return render(request, 'announcement.html', content)

# 软件启动图
@need_login
def startImgPage(request):
    setting = BasicSetting.objects.first()
    imgUrl = setting.imgStart
    content = {
        "title": "软件启动图",
        "startImg": imgUrl
    }
    return render(request, 'startimg.html', content)

# 软件退出图
@need_login
def exitImgPage(request):
    setting = BasicSetting.objects.first()
    imgUrl = setting.imgEnd
    content = {"title": "软件退出图", "exitImg": imgUrl}
    return render(request, 'exitimg.html', content)

# 系统设置
@need_login
def settingPage(request):
    data = AdminInfo.objects.first()
    content = {
        "title": "系统设置",
        "username": data.username,
        "password": data.password,
        "nickname": data.nickname,
        "avatar": data.avatar
    }
    return render(request, 'setting.html', content)

# 安装: 初始化数据
@need_login
def install(request):
    # 插入 软件基础设置 数据
    BasicSetting.objects.create(
        adtext="欢迎使用本软件，这里是广告位，10秒后消失！",
        showTime=10,
        imgStart="",
        imgEnd="",
        epgUrl="",
        ua="SYTV/1.6"
    )
    return JsonResponse({"code": 200, "msg": "初始化数据成功!"})

