from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


# Create your views here.

# def post_list(req):
#     posts = Post.published.all()
#     return render(req, 'blog/post/list.html', {'posts': posts})
def post_list(req):
    object_list = Post.published.all()
    # 3 posts in each page
    paginator = Paginator(object_list, 3)
    page = req.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range
        posts = paginator.page(paginator.num_pages)
    return render(req, 'blog/post/list.html', {'page': page, 'posts': posts})


def post_deatil(req, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)
    return render(req, 'blog/post/detail.html', {'post': post})
