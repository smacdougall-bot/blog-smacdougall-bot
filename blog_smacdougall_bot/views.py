from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse('Welcome to my blog!')

def home(request):
    """
    The Blog homepage
    """
    return render(request, 'blog/home.html')
