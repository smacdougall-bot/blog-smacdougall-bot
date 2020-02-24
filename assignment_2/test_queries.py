import string

from model_mommy import mommy
import pytest

from blog.models import Comment, Post
from . import queries

pytestmark = pytest.mark.django_db


def test_question_1_active_users(django_user_model):
    mommy.make(django_user_model, is_active=False)
    active = mommy.make(django_user_model, is_active=True)
    result = queries.question_1_return_active_users()

    assert list(result) == [active]


def test_question_2_regular_users(django_user_model):
    mommy.make(django_user_model, is_staff=True)
    mommy.make(django_user_model, is_superuser=True)
    user = mommy.make(django_user_model, is_staff=False, is_superuser=False)
    result = queries.question_2_return_regular_users()

    assert list(result) == [user]


def test_question_3_return_all_posts_for_user(django_user_model):
    mommy.make('blog.Post', _quantity=3)
    user = mommy.make(django_user_model)
    posts = mommy.make('blog.Post', author=user, _quantity=2)
    result = queries.question_3_return_all_posts_for_user(user)

    expected = Post.objects \
        .filter(pk__in=[obj.pk for obj in posts]) \
        .order_by('-created')

    assert list(result) == list(expected)


def test_question_4_returns_posts_ordered_by_title():
    posts = [
        mommy.make('blog.Post', title=letter)
        for letter in string.ascii_lowercase[:4]
    ]
    result = queries.question_4_return_all_posts_ordered_by_title()

    assert list(result) == posts


def test_question_5_returns_all_comments_for_post():
    mommy.make('blog.Comment', _quantity=2)
    post = mommy.make('blog.Post')
    comments = mommy.make('blog.Comment', post=post, _quantity=3)

    result = queries.question_5_return_all_post_comments(post)
    expected = list(reversed(comments))

    assert list(result) == expected


def test_question_6_returns_approved_comments():
    mommy.make('blog.Comment', approved=False)
    comment = mommy.make('blog.Comment', approved=True)
    result = queries.question_6_get_approved_comments_from_queryset()
    queryset_result = Comment.objects.approved()
    expected = [comment]

    assert list(result) == list(queryset_result) == expected


def test_question_7_search_post_text():
    mommy.make('blog.Post', _quantity=3)
    expression = 'my great expression'
    posts = [
        mommy.make('blog.Post', title='something about my great EXPRESSION'),
        mommy.make(
            'blog.Post',
            content='something something MY GREAT EXPRESSION'
        )
    ]
    result = queries.question_7_text_search_post_text(expression)

    assert list(result) == list(reversed(posts))


def test_question_8_post_with_most_comments():
    mommy.make('blog.Comment', _quantity=2)
    post = mommy.make('blog.Post')
    mommy.make('blog.Comment', post=post, _quantity=3)

    result = queries.question_8_return_the_post_with_the_most_comments()

    assert result == post


def test_question_9_create_a_comment_for_post():
    post = mommy.make('blog.Post')
    result = queries.question_9_create_a_comment(post)

    assert Comment.objects.filter(pk=result.pk, post=post).exists()


def test_question_10_set_comment_approved_false():
    comment = mommy.make('blog.Comment', approved=True)
    result = queries.question_10_set_approved_to_false(comment)
    comment.refresh_from_db()

    assert comment.approved is False


def test_question_11_delete_post_and_comments():
    post = mommy.make('blog.Post')
    mommy.make('blog.Comment', post=post, _quantity=2)
    result = queries.question_11_delete_post_and_all_related_comments(post)

    assert Post.objects.exists() is False
    assert Comment.objects.exists() is False
