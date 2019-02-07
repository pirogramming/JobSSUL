from django import forms
from django.core.validators import MinLengthValidator

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
