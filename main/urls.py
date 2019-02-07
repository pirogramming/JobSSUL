from django.urls import path

from main.views import main_detail, main_create, main_page, main_post

urlpatterns = [
    path('', main_page, name='main'),
    path('post/', main_post, name='post'),
    path('post/<int:pk>', main_detail, name='detail'),
    path('create/', main_create, name='create'),
]