from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from web.models import Post


def index(request):
    posts = Post.objects.order_by('-play_counts')
    paginator = Paginator(posts, 24)
    posts = paginator.page(1)

    return render(request, 'index.html', {'posts': posts})


def detail(request, pid):
    post = Post.objects.get(pid=pid)
    return render(request, 'post.html', {'post': post})