
from django.conf.urls import url

from django.urls import path
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views
from .Forms import LoginForm

app_name ='accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    # path('login/', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGIN_URL), name='logout'),


    path('mypage/', views.mypage, name='user_profile'),
    ]

