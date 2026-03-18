from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def registration(request):
    return render(request, 'registration.html')
# Create your views here.
