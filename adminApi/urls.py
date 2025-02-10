"""
URL configuration for adminApi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.views import static
import re


handler404 = views.notFound

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 前端视图路由
    path('admin/login', views.loginPage, name="login"),  #登录页面
    path('admin/main', views.mainPage),  # 后台首页
    path('admin/device', views.devicePage),  # 设备管理页面
    path('admin/soft/epg', views.epgPage),  # epg设置页面
    path('admin/soft/category', views.categoryPage),  # 分类管理页面
    path('admin/soft/channel', views.channelPage),  # 频道管理页面
    path('admin/soft/announcement', views.announcementPage),  # 公告管理页面
    path('admin/soft/startimg', views.startImgPage),  # 启动图管理页面
    path('admin/soft/exitimg', views.exitImgPage),  # 退出图管理页面
    path('admin/setting', views.settingPage),  # 系统设置页面
    path('admin/logout', views.logout),  # 登出

    # 后端操作路由
    path('api/install', views.install),  # 安装，初始化数据库
    path('api/device/', include('deviceAdmin.urls')),  # 设备管理相关
    path('api/soft/', include('softAdmin.urls')),  # 软件管理相关
    path('api/changePassword', views.changePassword),  # 修改密码

    # 前端软件路由
    path('api/android/', include('android.urls')),  # 软件对接接口

    # 404
    path('404', views.notFound),
    path('static/<path:path>', static.serve, {
        'document_root': settings.STATIC_ROOT
    }),
]
# DEBUG = False 时使用

