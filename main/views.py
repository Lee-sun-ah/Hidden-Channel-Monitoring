from django.shortcuts import render
from .models import First

# Create your views here.

def index(request):
    return render(request,'main/index.html')

def first(request):
    datas=First.objects.all()
    return render(request,'main/firstpage.html',{"datas":datas})
