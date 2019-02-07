from django.shortcuts import render

from main.models import Post

# Create your views here.


def main_post(request):
    post = Post.objects.all()
    data = {
        'post': post
    }
    return render(request, 'main.html', data)


def main_detail(request, pk):
    post = Post.objects.get(pk=pk)
    data = {
        'post': post,
    }
    return render(request, 'detail.html', data)

