from django.urls import path

from main.views import main_post

urlpatterns = [
    path('', main_post, name='main')
]