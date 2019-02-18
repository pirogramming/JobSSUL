from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import RequestContext
from django.views.decorators.http import require_POST
from .Forms import CommentForm
from .models import Post, Comment
from .Forms import PostForm
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse

def main_page(request):
    post = Post.objects.all()
    data = {
        'post': post
    }
    return render(request, 'main/main.html', data)


def main_post(request):
    # post = Post.objects.all()
    posts = Post.published.all()
    query = request.GET.get('q', None)
    print(query)
    if query:
        posts = Post.published.filter(
            Q(title__icontains=query) |
            Q(author__username=query) |
            Q(content__icontains=query)
            )
    data = {
        # 'post': post,
        'posts': posts,
    }
    return render(request, 'main/post.html', data)


def main_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    form = PostForm()

    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            message = request.POST.get('message')
            reply_id = request.POST.get('comment_id')
            comment_qs = None

            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)

            comment = Comment.objects.create(post=post, author=request.user, message=message, reply=comment_qs)
            comment.save()
            # return HttpResponseRedirect(post.get_absolute_url())
        else:
            comment_form = CommentForm()

    # comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    # comment_is_liked = False
    # for comment in comments:
    #     comment = comments.get()
    #     if comment.likes.filter(id=request.user.id).exists():
    #         comment_is_liked = True
    # comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))

    comment_is_liked = False
    for comment in comments:
        # comment_is_liked = False
        if comment.likes.filter(id=request.user.id).exists():
            comment_is_liked = True
    data = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
        'comments': comments,
        'comment_form': comment_form,
        'comment_is_liked': comment_is_liked,
        'form': form,

        # 'comment': comment,
    }

    if request.is_ajax():
        html = render_to_string('main/comments.html', data, request=request)
        return JsonResponse({'form': html})
    return render(request, 'main/detail.html', data)


def like_post(request):
    # post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post = get_object_or_404(Post, id=request.POST.get('id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    data = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
    }
    if request.is_ajax():
        html = render_to_string('main/like_section.html', data, request=request)
        return JsonResponse({'form': html})

def like_comment(request):
    # comment = get_object_or_404(Comment, id=request.POST.get('id'))
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    comment_is_liked = False
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        comment_is_liked = False
    else:
        comment.likes.add(request.user)
        comment_is_liked = True
        # return redirect(f'/main/post/{comment.post.pk}')
    # return redirect(f'/main/post/{comment.post.pk}')
    data = {
		'comment': comment
	}
    html = render_to_string('main/like_comment.html', data, request=request)
    return JsonResponse({'form': html})
    # return HttpResponseRedirect(comment.get_absolute_url())

@login_required
def main_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request=request)

        if form.is_valid():
            form.save()
            messages.info(request, '새 글이 등록되었습니다.')
            return redirect('main:post')
    else:
        form = PostForm(initial={'author': request.user})
    return render(request, 'main/create.html', {
        'form': form
    })

@login_required
def main_edit(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if post.author != request.user:
        return redirect(f'/main/post/{post.pk}')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(f'/main/post/{post.pk}')
    else:
        form = PostForm(instance=post)

    return render(request, 'main/edit.html', {
        'form': form,

    })


@login_required
def main_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if post.author != request.user:
        return redirect(f'/main/post/{post.pk}')

    if request.method == "POST":
        post.delete()
        return redirect('main:post')

    return render(request, 'main/delete.html', {
        'post': post
    })

@login_required
def comment_new(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, '댓글이 작성되었습니다.')
            return redirect('main:detail', post.pk)
    else:
        form = CommentForm()

    return render(request, 'main/comment_form.html', {
        'form': form,
    })

                  # , context_instance=RequestContext)


@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return redirect(f'/main/post/{comment.post.pk}') # '/main/post/{0}/'.format(comment.post.pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            comment = form.save()
            messages.success(request, '댓글이 수정되었습니다.')
            return redirect(f'/main/post/{comment.post.pk}')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'main/comment_form.html', {
        'form': form,
    })


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return redirect(f'/main/post/{comment.post.pk}')

    if request.method == 'POST':
        comment.delete()
        messages.error(request, '댓글이 삭제되었습니다.')
        return redirect(f'/main/post/{comment.post.pk}')

    return render(request, 'main/comment_confirm_delete.html', {
        'comment': comment,
    })
