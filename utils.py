from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

# 登录装饰器
def need_login(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # 检查会话中是否有登录状态
        if not request.session.get('logged_in', False):
            # 如果没有登录，重定向到登录页面
            return HttpResponseRedirect(reverse('login'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# 接口登录装饰器
def api_need_login(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # 检查会话中是否有登录状态
        if not request.session.get('logged_in', False):
            # 如果没有登录，重定向到登录页面
            return JsonResponse({"code": 403, "msg": "无权限"})
        return view_func(request, *args, **kwargs)
    return _wrapped_view