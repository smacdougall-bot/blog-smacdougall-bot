from django.shortcuts import render
from . import models
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello world!')

def home(request):
    """
    The Blog homepage
    """
    # Get last 3 posts
    latest_posts = models.Post.objects.published().order_by('-published')[:10]
    topics = models.Post.objects.get_topics()
    # Add as a context variable "latest_posts"
    context = {
        'topics': topics,
        'latest_posts': latest_posts
        }
    return render(request, 'blog/home.html', context)
