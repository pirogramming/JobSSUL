from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .Forms import UserCreationForm
from .models import *
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .Forms import UserCreationForm, LoginForm
from django.contrib.auth import login as auth_login


#회원가입
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(settings.LOGIN_URL)
        else:
            return render(request, 'accounts/signup_form.html', {
                'form': form,
            })
    else:
        form = UserCreationForm()
        return render(request, 'accounts/signup_form.html', {
        'form': form,
    })


#로그인
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

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
def mypage(request, username):
    if request.method =='GET':
        user = get_object_or_404(User, name=username)

        data = {
            'profile_user' : user,
        }
        return render(request, 'about.html', data)

