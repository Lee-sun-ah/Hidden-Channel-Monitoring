from django.shortcuts import render
from .models import TelChannel

# Create your views here.

def index(request):
    return render(request,'main/index.html')

def channel_info(request):
    datas=TelChannel.objects.all()
    return render(request,'main/channel_info.html',{"datas":datas})
