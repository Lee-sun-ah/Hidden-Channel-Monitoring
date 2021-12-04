from django.contrib import admin
from django.urls import path,include
from . import views

app_name="main"

urlpatterns = [
    path('',views.index,name='index'),
    path('result',views.result,name='result'),
    path('users_info',views.users_info,name='users_info'),
    path('messages_info',views.messages_info,name='messages_info')
]
