from django.shortcuts import render,HttpResponse,redirect
from . import models
# Create your views here.

def hello(request):
    article = models.Article.objects.get(pk=1)
    return render(request,'templates/index.html',{'key':article })