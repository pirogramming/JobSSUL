from django.contrib import admin

from .models import Comment
from main.models import Post

admin.site.register(Post)


@admin.register(Comment)


class CommentAdmin(admin.ModelAdmin):
    pass

