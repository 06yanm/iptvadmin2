from django import template
from adminApi.models import AdminInfo

register = template.Library()

@register.simple_tag
def global_nickname():
    d = AdminInfo.objects.first()
    return d.nickname

@register.simple_tag
def global_avatar():
    d = AdminInfo.objects.first()
    return d.avatar