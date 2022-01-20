from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView


# Create your views here.
class PoatListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'
    paginate_by = 3

# def post_list(request):
#     posts = Post.published.all()
#     return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    return render*request, 'blog/post_detail.html', {'post': post}