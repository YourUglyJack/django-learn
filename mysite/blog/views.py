from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm
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


# def post_share(req, post_id):
#     # retrieve post by id
#     post = get_object_or_404(Post, id=post_id, status='published')
#     if req.method == 'Post':
#         # form was submitted
#         form = EmailPostForm(req.POST)
#         if form.is_valid():
#             # form fields passed validation
#             cd = form.cleaned_data
#             # ... send email
#     else:
#         form = EmailPostForm()
#     return render(req, 'blog/post/share.html', {'post': post, 'form': form})
def post_share(req, post_id):
    # retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    send = False
    if req.method == 'Post':
        # form was submitted
        form = EmailPostForm(req.Post)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = req.build_abosolut_url(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read" \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url} \n\n" \
                      f"{cd['name']}\'s comments:{cd['comments']}"
            send_mail(subject, message, 'leety589589@163.com', [cd['to']])
        send = True
    else:
        form = EmailPostForm()
    print('send',send)
    return render(req, 'blog/post/share.html', {'post': post, 'form': form, 'send': send})


def send_email(req):
    # 目前好像没啥用
    send_mail(
        subject='Title',
        message='This is a text from django',
        from_email='leety589589@163.com',
        recipient_list=['1091349400@qq.com'],
        fail_silently=False
    )
    return HttpResponse('Ok')


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
