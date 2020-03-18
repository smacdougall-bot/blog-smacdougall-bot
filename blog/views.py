from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render
from . import models


def index(request):
    return HttpResponse('Hello world!')

def terms_and_conditions(request):
    return render(request, 'blog/terms_and_conditions.html')

class PostListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')  # Customized queryset

class TopicsListView(ListView):
    model = models.Topic
    

class PostDetailView(DetailView):
    model = models.Post
    context_object_name = 'post'
    def get_queryset(self):
        queryset = super().get_queryset().published()

        # If this is a `pk` lookup, use default queryset
        if 'pk' in self.kwargs:
            return queryset

        # Otherwise, filter on the published date
        return queryset.filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )

class HomeView(TemplateView):
    """
    The Blog homepage
    """
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        # get the parent context
        context = super().get_context_data(**kwargs)
        # Get last 10 posts
        latest_posts = models.Post.objects.published().order_by('-published')[:10]
            # Add context variables
        context.update({
            'latest_posts': latest_posts
        })
        return context


class AboutView(TemplateView):
    template_name = 'blog/about.html'
