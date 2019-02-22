from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


from .models import *
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.urls import reverse
from .Forms import UserCreationForm, LoginForm, UpdateProfile
from main.models import Post, Comment
from main.views import scrap_post
from django.contrib.auth import login as auth_login


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(settings.LOGIN_URL)
        else:
            messages.error(request, '정보를 정확히 입력해주세요.')
            return render(request, 'accounts/signup_form.html', {
                'form': form
            })
    else:
        form = UserCreationForm()
        return render(request, 'accounts/signup_form.html', {
                'form': form,
    })


#로그인
def main_login(request):
    if request.method == "POST":
        form = LoginForm()
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('main:main')
        else:
            messages.error(request, '로그인 실패. 다시 시도 해보세요.')
            return redirect('accounts:login')
    else:
        form = LoginForm()
        return render(request, 'accounts/login_form.html',{
            'form': form
        })

      
@login_required
def mypage(request):
    if request.method =='GET':
        user = request.user
        user_posts = Post.objects.filter(author=user)
        scrap_posts=user.scrap.all()
        user_comments = Comment.objects.filter(author=user)
        data = {
            'profile_user': user,
            'my_posts': user_posts,
            'my_comments': user_comments,
            'scrap_posts':scrap_posts,
        }
        return render(request, 'accounts/about.html', data)

@login_required
def edit_mypage(request):
    args={}
    if request.method=='POST':
        form=UpdateProfile(request.POST, instance=request.user)
        form.actual_user=request.user
        if form.is_valid():
            form.save()
            return redirect('accounts:user_profile')
    else:
        form = UpdateProfile()

    args['form']=form
    return render(request, 'accounts/edit_mypage.html', args)