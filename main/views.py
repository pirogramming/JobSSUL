from django.shortcuts import render

from main.models import Post

def main_post(request):
    post = Post.objects.all()
    data = {
        'post': post
    }
    return render(request, 'main.html', data)

# Create your views here.
