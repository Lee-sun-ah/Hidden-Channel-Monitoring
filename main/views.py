from django.shortcuts import render
from .models import First

# Create your views here.

def index(request):
    datas=First.objects.all()
    return render(request,'main/index.html',{"datas":datas})
