from django import template
from ..models import Post, Comment

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag("blog/latest_posts.html")
def show_latest_posts(count=5):
    latest_posts = Post.published.all()[:count]
    return {"latest_posts": latest_posts}


@register.inclusion_tag("blog/latest_comments.html")
def show_latest_comments(count=5):
    latest_comments = Comment.objects.all().order_by("-created")
    return {"latest_comments": latest_comments}
