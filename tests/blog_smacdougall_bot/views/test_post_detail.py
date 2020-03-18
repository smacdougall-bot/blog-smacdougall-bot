from model_mommy import mommy
import pytest
from blog.models import Post


pytestmark = pytest.mark.django_db


def test_post_detail_view_is_accessed_by_date_and_slug(client):
    mommy.make(
        'blog.Post',
        slug='happy-halloween',
        status=Post.PUBLISHED,
        published='2019-10-31T00:00Z',
    )

    response = client.get('/posts/2019/10/31/happy-halloween/')
    assert response.status_code == 200


def test_post_detail_filters_by_date(client):
    """
    Given two posts with the same slug, but different published
    dates, the response code should be 200.
    """
    mommy.make(
        'blog.Post',
        title='2019 Halloween',
        slug='happy-halloween',
        status=Post.PUBLISHED,
        published='2019-10-31T00:00Z',
    )
    mommy.make(
        'blog.Post',
        title='2020 Halloween',
        slug='happy-halloween',
        status=Post.PUBLISHED,
        published='2020-10-31T00:00Z',
    )

    response = client.get('/posts/2019/10/31/happy-halloween/')
    assert response.status_code == 200


def test_post_detail_returns_404_for_drafts(client):
    mommy.make(
        'blog.Post',
        slug='happy-new-year',
        published='2020-01-01T00:00Z',
        status=Post.DRAFT
    )
    response = client.get('/posts/2020/1/1/happy-new-year/')
    assert response.status_code == 404

def test_post_detail_by_pk_without_published_date(client):
    post = mommy.make('blog.Post', status=Post.PUBLISHED)
    response = client.get(f'/posts/{post.pk}/')
    assert response.status_code == 200
