from django.urls import path, re_path
from . import views


app_name= 'notice'

urlpatterns = [
    path('', views.main_page, name='main')
    # path('post/<int:post_pk>/', views.main_detail, name='detail'),
    # path('create/', main_create, name='create'),
    # path('post/<int:post_pk>/edit/', views.main_edit , name='edit'),
    # path('post/<int:post_pk>/delete/', views.main_delete , name='delete'),
]