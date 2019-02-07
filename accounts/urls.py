from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from .Forms import LoginForm


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login_form.html', authentication_form = LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGIN_URL), name='logout'),
]
