from django.conf import settings  # Imports Django's loaded settings
from django.db import models
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.
class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=self.model.PUBLISHED)

    def get_topics(self):
        topics_count = Topic.objects.annotate(total_posts=Count('blog_posts'))
        return topics_count.values('name', 'total_posts')

    def get_authors(self):
        User = get_user_model()
        # Get the users who are authors of this queryset
        return User.objects.filter(blog_posts__in=self).distinct()

class CommentQuerySet(models.QuerySet):
    def approved(self):
        return self.exclude(approved=False)



class Topic(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True  #No Dupilcates
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    name = models.CharField(
        null=False,
        max_length=50
    )
    email = models.EmailField(
        null=False,
    )

    text = models.CharField(
        null=False,
        max_length=500
    )
    approved = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    objects = CommentQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']



class Post(models.Model):
    '''
    Represents a blog post
    '''
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Ths Django auth user model
        on_delete=models.PROTECT, # Prevent posts from being deleted
        related_name='blog_posts', # "This" on the user models
        null=False
    )
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make post publicly visible',
    )

    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date and time this article was published',
    )


    slug = models.SlugField(
        null=False,
        help_text='Human readable URL path',
        unique_for_date='published', # Slug is unique for publication date
    )
    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts'
    )

    objects = PostQuerySet.as_manager()

    def publish(self):
        """Publishes this post"""
        self.status = self.PUBLISHED
        self.published = timezone.now() # The current datetime with timezone

    def get_absolute_url(self):
        if self.published:
            kwargs = {
                'year': self.published.year,
                'month': self.published.month,
                'day': self.published.day,
                'slug': self.slug
            }
        else:
            kwargs = {'pk': self.pk}

        return reverse('post-detail', kwargs=kwargs)

    class Meta:
        # Sort by the `created` field. The `-` prefix
        # specifies to order in descending/reverse order.
        # Otherwise, it will be in ascending order.
        ordering = ['-created']

    def __str__(self):
        return self.title
