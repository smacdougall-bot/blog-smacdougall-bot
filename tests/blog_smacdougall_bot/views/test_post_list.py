import pytest
from model_mommy import mommy
from blog.models import Post


pytestmark = pytest.mark.django_db

def test_post_list_url_returns_200(client):
    response = client.get('/posts/')
    assert response.status_code

def test_post_list_only_returns_published_articles(client):
    published = mommy.make(
        'blog.Post',
        status=Post.PUBLISHED,
        title='Published post'
    )
    mommy.make(
        'blog.Post',
        status=Post.DRAFT,
        title='Draft post'
    )

    response = client.get('/posts/')
    # Get the posts object_list
    result = response.context.get('posts')

    assert list(result) == [published]


def test_post_list_returns_latest_first(client):
    latest = mommy.make(
        'blog.Post',
        status=Post.PUBLISHED,
        published='2020-01-01T00:00:00Z',
        title='Happy 2020!'
    )
    earliest = mommy.make(
        'blog.Post',
        status=Post.PUBLISHED,
        published='2019-01-01T00:00:00Z',
        title='Happy 2019!',
    )
    response = client.get('/posts/')
    result = response.context.get('posts')
    expected = [latest, earliest]

    assert list(result) == expected
