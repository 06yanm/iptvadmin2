from django.urls import path
from android import views

urlpatterns = [
    path("getData", views.getinfo),
    path("getLive", views.getlive),
    path("getLogo/<str:name>", views.getlogo),
    # path("getMiniData", views.getMiniData)
]