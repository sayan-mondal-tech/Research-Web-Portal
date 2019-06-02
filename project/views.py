from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request,'project/index.html')

def about(request):
    return HttpResponse('<h1>About</h1>')

def login_f(request):
    return render(request,'project/login_f.html')

def login_s(request):
    return render(request,'project/login_s.html')
