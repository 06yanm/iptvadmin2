from django.urls import path
from . import views


urlpatterns = [
    path('getDevicesByPage', views.getDeviceByPage),  # 根据页码获取设备列表
    path('authByIds', views.authByIds),  # 根据设备id批量授权
    path('unAuthByIds', views.unAuthByIds),  # 根据设备id批量授权
    path('changeCateMany', views.changeCateMany),  # 批量修改设备可看分类
    path('getDevicePageNum', views.getDevicePageNum),  # 获取设备总页数
]