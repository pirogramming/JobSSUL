
from django.urls import path, re_path
from . import views
from main.views import main_detail, main_create

app_name='main'

urlpatterns = [
    path('', views.main_page, name='main'),
    path('post/', views.main_post, name='post'),
    path('post/<int:post_pk>/', views.main_detail, name='detail'),
    path('create/', main_create, name='create'),
    path('post/<int:post_pk>/edit/', views.main_edit , name='edit'),
    path('post/<int:post_pk>/delete/', views.main_delete , name='delete'),
    path('post/<int:post_pk>/comment/new/', views.comment_new, name='comment_new'),
    path('post/<int:pk>/comment/edit/', views.comment_edit, name='comment_edit'),
    path('post/<int:pk>/comment/delete/', views.comment_delete, name='comment_delete'),
    path('like/', views.like_post, name='like_post'),
    # path('post/<int:pk>/comment/like_comment/', views.like_comment, name='like_comment'),
    path('like_comment/', views.like_comment, name='like_comment'),
]
