from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import *

# Create your views here.
from django.views.generic import TemplateView

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(redirect(settings.LOGIN_URL))
    else:
        form = UserCreationForm()

        return render(request, 'accounts/signup_form.html', {
        'form': form,
    })

@login_required
def mypage(request, username):
    if request.method =='GET':
        user = get_object_or_404(User, name=username)

        data = {
            'profile_user' : user,
        }
        return render(request, 'about.html', data)
