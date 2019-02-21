from itertools import chain

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import RequestContext
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from .Forms import CommentForm
from .models import Post, Comment
from .Forms import PostForm
from django.db.models import Q, Count, QuerySet
from django.template.loader import render_to_string
from django.http import JsonResponse




def main_page(request):
    posts = Post.objects.all()
    # posts = Post.objects.all().order_by('-updated_at')
    data = {
        'posts': posts,
        'latest': posts.order_by('-updated_at'),
        'liked': posts.annotate(liked=Count('likes')).order_by('-liked'),

    }
    return render(request, 'main/main.html', data)


def main_post(request):
    # post = Post.objects.all()
    posts = Post.published.all()
    query = request.GET.get('q', None)
    # post = get_object_or_404(Post, id=request.POST.get('id'))
    # comments = Comment.objects.filter()
    # post_comments_count = Comment.objects.filter(post=post).count()

    # for post in posts:
    #     post = get_object_or_404(Post, id=request.POST.get('id'))
    # comments_count = Comment.objects.filter(post_id=post_id).count()

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(author__username=query) |
            Q(content__icontains=query)
            )
    data = {
        # 'post': post,
        'posts': posts,
        # 'comments': comments,
        # 'post': post,
        # 'post_comments_count': post.post_comments_count()
        # 'comments_count': comments_count,
        # 'post_id': post_id,
    }
    return render(request, 'main/post.html', data)


def main_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    form = PostForm()

    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')

    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    is_scrap = False
    if post.scrap.filter(id=request.user.id).exists():
        is_scrap = True

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
        'is_scrap': is_scrap,

        # 'comment': comment,
    }

    if request.is_ajax():
        html = render_to_string('main/comments.html', data, request=request)
        return JsonResponse({'form': html})
    return render(request, 'main/detail.html', data)


def scrap_post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if post.scrap.filter(pk=request.user.id).exists():
        post.scrap.remove(request.user)
        is_scrap = False
    else:
        post.scrap.add(request.user)
        is_scrap = True

    data = {
        'is_scrap': is_scrap,
        'post': post,
    }

    if request.is_ajax():
        html = render_to_string('main/scrap.html', data, request=request)
        return JsonResponse({'form': html})


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
        print('되나')
        if form.is_valid():
            print('됐네')
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


def best_post(request):
    posts = Post.objects.all()
    # posts = Post.objects.filter.order_by('-likes', '-updated_at')

    return render(request, 'main/best_post.html', {
        'posts': posts
    })


def category(request):
        posts = Post.objects.all()
        place = request.POST.get('place', '0')
        type = request.POST.get('type', '0')
        pay = request.POST.get('pay', '0')

        if place == '0' or type == '0' or pay == '0':
            messages.error(request, '세 카테고리를 모두 선택해주세요')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        #조건들 선택안하고 그냥 누르면 request한 그 해당 페이지 리턴

        list1 = place.split('/')
        result = set()
        if place:
            for point in list1:
                posts = set(Post.objects.filter(
                    Q(reside__icontains=point)
                ))
                result = result | posts
            posts = result

        if type != '전체':
            result = set()
            for post in posts:
                if post.work_type == type:
                    result.add(post)
            posts = result

        if pay != '전체':
            result = set()
            for post in posts:
                if post.payment == pay:
                    result.add(post)

        data = {
            'posts': result,
        }

        return render(request, 'main/category_list.html', data)

