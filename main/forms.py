from django import forms
from django.core.validators import MinLengthValidator

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('likes', 'author')


class CommentForm(forms.ModelForm):
    message = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '내용을 입력하세요!', 'rows': '4', 'cols': '50'}))
    class Meta:
        model = Comment
        fields = ['message']

