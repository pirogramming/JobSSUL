from django.urls import path, re_path
from . import views
from main.views import main_post, main_detail

app_name = 'main'

urlpatterns = [
    path('', main_post, name='main'),
    path('<int:pk>', main_detail, name='detail'),
    re_path(r'^(?P<post_pk>\d+)/comment/new/$', views.comment_new, name='comment_new'),
    re_path(r'^(?P<post_pk>\d+)/comment/(?P<pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),
    re_path(r'^(?P<post_pk>\d+)/comment/(?P<pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),

]