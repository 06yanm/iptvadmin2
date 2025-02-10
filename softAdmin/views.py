import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from sympy import false
from android.models import  BasicSetting
from .models import Category, Channel
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from utils import need_login, api_need_login

LIMIT = 10

# 获取频道数量
def getChannelCount():
    count = Channel.objects.count()
    return count

# 获取分类数量
def getCategoryCount():
    count = Category.objects.count()
    return count

# 编辑频道
@api_need_login
def editChannel(request):
    if request.method == 'POST':
        id = request.POST.get('eid')
        name = request.POST.get('ename')
        url = request.POST.get('eurl')
        desc = request.POST.get('edesc')
        cid = request.POST.get('ecid')
        hidden = request.POST.get('ehidden')
        if hidden == 0 or hidden == '0':
            hidden = True
        else:
            hidden = False
        if not id or not name or not url or not cid:
            return JsonResponse({"code": 400, "msg": "缺少参数"})
        if not Category.objects.filter(id=cid).exists():
            return JsonResponse({"code": 400, "msg": "分类不存在"})
        if Channel.objects.filter(name=name).exclude(id=id).exists():
            return JsonResponse({"code": 400, "msg": "频道名称已存在"})
        category = Category.objects.get(id=cid)
        Channel.objects.filter(id=id).update(name=name, url=url, desc=desc, category=category, hidden=hidden)
        return JsonResponse({"code": 200, "msg": "修改成功"})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误！"})

# 批量上下架
@api_need_login
def showCahnnel(request):
    if request.method == 'POST':
        ids = request.POST.get('ids')
        cz = request.POST.get('cz')
        if ids:
            ids = json.loads(ids)
            if cz == "sj":
                Channel.objects.filter(id__in=ids).update(hidden=False)
                return JsonResponse({"code": 200, "msg": "上架成功"})
            else:
                Channel.objects.filter(id__in=ids).update(hidden=True)
                return JsonResponse({"code": 200, "msg": "下架成功"})

        else:
            return JsonResponse({"code": 400, "msg": "缺少参数"})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误！"})

# 获取频道分页数量
@api_need_login
def getChannelPageNum(request):
    if request.method == 'GET':
        num = getChannelsByPageMethod(1)[1]
        return JsonResponse({"code": 200, "msg": "获取成功", "data": num})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误！"})

# 批量删除频道
@api_need_login
def delChannel(request):
    if request.method == 'POST':
        ids = request.POST.get('ids')
        if ids:
            ids = json.loads(ids)
            Channel.objects.filter(id__in=ids).delete()
            return JsonResponse({"code": 200, "msg": "删除成功"})
        else:
            return JsonResponse({"code": 400, "msg": "缺少参数"})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误！"})

# 新增频道
@api_need_login
def addChannel(request):
    if request.method == 'POST':
        name = request.POST.get('addname')
        desc = request.POST.get('adddesc')
        cate = request.POST.get('addcate')
        url = request.POST.get('addurl')
        if not name or not cate or not url:
            return JsonResponse({"code": 400, "msg": "缺少参数"})
        if Channel.objects.filter(name=name).exists():
            return JsonResponse({"code": 401, "msg": "频道已存在"})
        hidden = false
        if desc == "" or not desc:
            desc = ""
        Channel.objects.create(name=name, desc=desc, category_id=cate, url=url, hidden=hidden)
        return JsonResponse({"code": 200, "msg": "新建频道成功"})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误！"})


# 根据页码获取所有频道(方法)
def getChannelsByPageMethod(page):
    channels = Channel.objects.all().order_by('id')
    paginator = Paginator(channels, LIMIT)
    try:
        channels = paginator.page(page)
    except PageNotAnInteger:
        channels = paginator.page(1)
    except EmptyPage:
        channels = paginator.page(paginator.num_pages)
    channelList = []
    num = (int(page) - 1) * LIMIT
    for channel in channels:
        num += 1
        if channel.desc =="":
            desc = "无"
        else:
            desc = channel.desc
        channelList.append({
            "num": num,
            "id": channel.id,
            "name": channel.name,
            "desc": desc,
            "status": channel.hidden,
            "cate": channel.category.name,
            "url": channel.url
        })
    return channelList, paginator.num_pages

# 根据页码获取频道(接口)
@api_need_login
def getChannelsByPage(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        data = getChannelsByPageMethod(page)[0]
        return JsonResponse({"code": 200, "msg": "获取成功！", "data": data})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误！"})


# 根据分类id修改分类描述，名称
@api_need_login
def editCategory(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        if not id or id == "":
            return JsonResponse({"code": 401, "msg": "请选择要修改的分类！"})
        if not name or name == "":
            return JsonResponse({"code": 402, "msg": "分类名称不能为空！"})
        if Category.objects.filter(name=name).exclude(id=id).exists():
            return JsonResponse({"code": 403, "msg": "分类名称已存在！"})
        Category.objects.filter(id=id).update(name=name, desc=desc)
        return JsonResponse({"code": 200, "msg": "修改成功！"})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误！"})

# 获取分类总页数
@api_need_login
def getCategoryPageNum(request):
    if request.method == 'GET':
        num = getCategoriesByPageMethod(1)[1]
        return JsonResponse({"code": 200, "msg": "获取成功！", "data": num})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误！"})

# 批量删除分类
@api_need_login
def delCategory(request):
    if request.method == 'POST':
        ids = json.loads(request.POST.get('ids'))
        if not ids or ids == []:
            return JsonResponse({"code": 401, "msg": "请选择要删除的分类！"})
        else:
            Category.objects.filter(id__in=ids).delete()
            return JsonResponse({"code": 200, "msg": "删除成功！"})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误！"})


# 添加分类
@api_need_login
def addCategory(request):
    if request.method == 'POST':
        name = request.POST.get('CateName')
        desc = request.POST.get('CateDesc')
        if name == "" or not name:
            return JsonResponse({"code": 401, "msg": "分类名称不能为空！"})
        if Category.objects.filter(name=name).exists():
            return JsonResponse({"code": 402, "msg": "分类名称已存在！"})
        Category.objects.create(name=name, desc=desc)
        return JsonResponse({"code": 200, "msg": "添加成功！"})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误！"})

# 获取所有分类(方法)
def getAllCategory():
    d = Category.objects.all()
    names = []
    for i in d:
        names.append(
            {
                "id": i.id,
                "name": i.name,
                "desc": i.desc,
            }
        )
    return names

# 根据page获取分类(方法)
def getCategoriesByPageMethod(page):
    allCates = Category.objects.all().order_by('-id')
    paginator = Paginator(allCates, LIMIT)
    try:
        cates = paginator.page(page)
    except PageNotAnInteger:
        cates = paginator.page(1)
    except EmptyPage:
        cates = paginator.page(paginator.num_pages)
    catesList = []
    num = (int(page) - 1) * LIMIT
    for cate in cates:
        num += 1
        channels = ",".join(str(value.name) for value in cate.channels.all())
        if cate.channels.all().count() == 0:
            channels = "无"
        if cate.desc == "":
            desc = "无"
        else:
            desc = cate.desc
        catesList.append(
            {
                "num": num,
                "id": cate.id,
                "desc": desc,
                "name": cate.name,
                "channelsNum": cate.channels.all().count(),
                "channels": channels
            }
        )
    return catesList, paginator.num_pages


# 根据page获取分类(接口)
@api_need_login
def getCategoriesByPage(request):
    if request.method == 'GET':
        page = request.GET.get('page', '1')
        data = getCategoriesByPageMethod(page)
        return JsonResponse({"code": 200, "msg": "获取成功！", "data": data[0]})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误！"})




# EPG修改接口
@api_need_login
def epg(request):
    if request.method == 'POST':
        epg = request.POST.get("epg")
        if not epg:
            return JsonResponse({"code": 401, "msg": "数据为空或数据不合法！"})
        d = BasicSetting.objects.first()
        d.epgUrl = epg
        d.save()
        return JsonResponse({"code": 200, "msg": "修改成功！"})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误！"})

# 公告修改接口
@api_need_login
def announcement(request):
    if request.method == 'POST':
        content = request.POST.get("content")
        showtime = request.POST.get("showtime")
        if not showtime.isdigit() or not content or not showtime:
            return JsonResponse({"code": 401, "msg": "数据为空或数据不合法！"})
        d = BasicSetting.objects.first()
        d.adtext = content
        d.showTime = showtime
        d.save()
        return JsonResponse({"code": 200, "msg": "修改成功！"})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误！"})


# 启动图接口
@api_need_login
def startImg(request):
    if request.method == 'POST':
        img = request.POST.get("startImg")
        if not img:
            return JsonResponse({"code": 401, "msg": "数据为空或数据不合法！"})
        d = BasicSetting.objects.first()
        d.imgStart = img
        d.save()
        return JsonResponse({"code": 200, "msg": "修改成功！"})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误！"})

# 退出图接口
@api_need_login
def exitImg(request):
    if request.method == 'POST':
        img = request.POST.get("exitImg")
        if not img:
            return JsonResponse({"code": 401, "msg": "数据为空或数据不合法！"})
        d = BasicSetting.objects.first()
        d.imgEnd = img
        d.save()
        return JsonResponse({"code": 200, "msg": "修改成功！"})
    else:
        return JsonResponse({"code": 500, "msg": "请求方式错误！"})