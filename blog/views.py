from django.http import HttpResponse
from django.shortcuts import render
from . import models

def index(request):
    return HttpResponse('Welcome to my blog!')

def home(request):
    """
    The Blog homepage
    """
    # Get last 3 posts
    latest_posts = models.Post.objects.published().order_by('-published')[:3]
    # Add as a context variable "latest_posts"
    context = {'latest_posts': latest_posts}
    return render(request, 'blog/home.html')
