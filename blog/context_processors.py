from . import models

def base_context(request):
    authors = models.Post.objects.published() \
        .get_authors() \
        .order_by('first_name')
    topics = models.Post.objects.get_topics().order_by('-total_posts')
    topics_name_sort = models.Post.objects.get_topics().order_by('name')
    return{
        'authors': authors,
        'topics': topics,
        'topics_name_sort': topics_name_sort,
        }
