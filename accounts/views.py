from django.conf import settings
from django.shortcuts import render, redirect

from django.urls import reverse

from .Forms import UserCreationForm
from django.contrib.auth.views import LoginView
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from .Forms import LoginForm


def signup(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('main:main'))
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form,
    })


auth_login = LoginView.as_view()
#잠시만
def login(request):
    providers = []
    for provider in get_providers():
        try:
            provider.social_app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)
        except SocialApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)

    return auth_login(request,
                      authentication_form=LoginForm,
                      template_name='accounts/login_form.html',
                      extra_context={'providers':providers})


