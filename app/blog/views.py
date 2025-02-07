from datetime import datetime

from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import FormView
from taggit.models import Tag

from .forms import CommentsForm, ContactMeForm, SearchForm
from .models import Post

# Create your views here.
# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     template_name = 'blog/post_list.html'
#     paginate_by = 5


def inject_form(request):
    return {"search_form": SearchForm()}


def post_list(request, tag_slug=None):
    """List published posts from the most recent"""
    object_list = Post.published.all()
    tag = None
    date = datetime.now()
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 10)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        "blog/post_list.html",
        {"posts": posts, "page": page, "tag": tag, "date": date},
    )


def about(request):
    return render(request, "blog/about.html")


class ContactFormView(FormView):
    template_name = "blog/contact_me.html"
    form_class = ContactMeForm
    success_url = "/"

    def form_valid(self, form):
        # if form is valid, send a mail
        form.send_email()
        return super().form_valid(form)


# def contact_me(request):
#     contact_form = ContactMeForm()
#     if request.method == "POST":
#         contact_form = ContactMeForm(data=request.POST)
#         if contact_form.is_valid():
#             subject = "Blog Inquiry"
#             body = {
#                 "name": contact_form.cleaned_data["name"],
#                 "email": contact_form.cleaned_data["email"],
#                 "message": contact_form.cleaned_data["message"],
#             }
#             message = "\n".join(body.values())
#
#             try:
#                 contact_form.send_email()
#                 messages.success(request, "Email sent successfully")
#             except BadHeaderError:
#                 return HttpResponse("Invalid Header Found")
#             return redirect("blog:home")
#
#     return render(request, "blog/contact_me.html", {"form": contact_form})


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
        Post.published.select_related("author"),
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == "POST":
        comment_form = CommentsForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentsForm()
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count(F("tags"))).order_by(
        "-same_tags", "-publish"
    )[:4]

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
            "similar_posts": similar_posts,
        },
    )


def post_search(request):
    search_form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data["query"]
            search_vector = SearchVector("title", weight="A") + SearchVector(
                "body", weight="B"
            )
            search_query = SearchQuery(query)
            results = (
                Post.published.annotate(
                    rank=SearchRank(search_vector, search_query),
                    similarity_title=TrigramSimilarity("title", query),
                    similarity_body=TrigramSimilarity("body", query),
                )
                .filter(
                    Q(rank__gte=0.3)
                    | Q(similarity_title__gt=0.1)
                    | Q(similarity_body__gt=0.3)
                )
                .order_by("-rank")
            )
            # if results:
            #     results = results
            # else:
            #     results = Post.published.annotate(
            #         similarity_title=TrigramSimilarity(
            #             'title', search_query), similarity_body=TrigramSimilarity('body', search_query)) \
            #         .filter(Q(similarity_title__gt=0.1) | Q(similarity_body__gt=0.7)) \
            #         .order_by('-similarity_title')
    return render(
        request,
        "blog/search_results.html",
        {"search_form": search_form, "query": query, "results": results},
    )
