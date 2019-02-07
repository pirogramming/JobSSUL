from django.shortcuts import render, redirect

from main.form import PostForm
from main.models import Post

# Create your views here.


def main_page(request):
    post = Post.objects.all()
    data = {
        'post': post
    }
    return render(request, 'main/main.html', data)


def main_post(request):
    post = Post.objects.all()
    data = {
        'post':post
    }
    return render(request, 'main/post.html', data)

def main_detail(request, pk):
    post = Post.objects.get(pk=pk)
    data = {
        'post': post,
    }
    return render(request, 'main/detail.html', data)


def main_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        # title = request.POST.title
        # content = request.POST.content
        # payment = request.POST.payment
        # workplace = request.POST.payment
        # recommend = request.POST.recommend
        # work_type = request.POST.work_type

        if form.is_valid():
            post = Post.objects.create(title = form.cleaned_data['title'], content=form.cleaned_data['content'],
                                       payment = form.cleaned_data['payment'], workplace = form.cleaned_data['recommend'],
                                       work_type = form.cleaned_data['work_type'], recommend = form.cleaned_data['recommend'])
            return redirect('main')
    else:
        form = PostForm()
    return render(request, 'main/create.html', {
        'form': form,
    })



