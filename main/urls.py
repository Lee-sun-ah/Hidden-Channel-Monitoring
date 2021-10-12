from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('channel_info/',views.channel_info,name='channel_info'),
]
