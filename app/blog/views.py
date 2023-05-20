from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, F, Q
from django.contrib.postgres.search import TrigramSimilarity, SearchVector, SearchQuery, SearchRank

from taggit.models import Tag, TaggedItem

from .forms import CommentsForm, EmailPostForm, SearchForm, PostForm
from .models import Post, UUIDTaggedItem
# Create your views here.
# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     template_name = 'blog/post_list.html'
#     paginate_by = 5


def inject_form(request):
    return ({'search_form': SearchForm()})


def post_list(request, tag_slug=None):
    """List published posts from the most recent"""
    object_list = Post.published.all()
    tag = None
    date = datetime.now()
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = TaggedItem.objects.filter(tag=tag, content_type__model='post') \
            .values_list('object_id', flat=True)
        object_list = object_list.filter(id__in=object_list)
        # object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'posts': posts,
                                                   'page': page,
                                                   'tag': tag,
                                                   'date': date})


def post_detail(request, year, month, day, post):
    # post = get_object_or_404(
    #     Post,
    #     slug=post,
    #     status='published',
    #     publish__year=year,
    #     publish__month=month,
    #     publish__day=day
    # )
    post = get_object_or_404(
        Post.published.select_related('author'),
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentsForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentsForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count(F('tags'))) \
        .order_by('-same_tags', '-publish')[:4]

    return render(request,
                  'blog/post_detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})


def post_search(request):
    search_form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            search_vector = (
                SearchVector('title', weight='A') +
                SearchVector('body', weight='B')
            )
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                rank=SearchRank(search_vector, search_query),
                similarity_title=TrigramSimilarity(
                    'title', query), similarity_body=TrigramSimilarity('body', query)) \
                .filter(Q(rank__gte=0.3) | Q(similarity_title__gt=0.1) | Q(similarity_body__gt=0.3)) \
                .order_by('-rank')
            # if results:
            #     results = results
            # else:
            #     results = Post.published.annotate(
            #         similarity_title=TrigramSimilarity(
            #             'title', search_query), similarity_body=TrigramSimilarity('body', search_query)) \
            #         .filter(Q(similarity_title__gt=0.1) | Q(similarity_body__gt=0.7)) \
            #         .order_by('-similarity_title')
    return render(request,
                  'blog/search_results.html',
                  {'search_form': search_form,
                   'query': query,
                   'results': results})
