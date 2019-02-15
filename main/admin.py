from django.contrib import admin

from main.Forms import PostForm
from .models import Comment
from main.models import Post

@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    form = PostForm

@admin.register(Comment)



class CommentAdmin(admin.ModelAdmin):
    pass

