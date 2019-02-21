from django import forms
from django.core.validators import MinLengthValidator
from django.forms import TextInput, HiddenInput, Textarea

from main.widgets import RateitjsWidget

from jobssul.widgets.daum_address_widget import DaumAddressWidget
from .models import Post, Comment


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PostForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['likes', 'author', 'scrap']
        widgets = {
            'recommend': RateitjsWidget,
            'status': TextInput(attrs={'readonly': True}),
            'reside': DaumAddressWidget()
        }

    def save_create(self, commit=True):
        self.instance.author = self.request.user
        return super().save(commit=commit)


class CommentForm(forms.ModelForm):
    message = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '내용을 입력하세요!', 'rows': '4', 'cols': '50'}))

    class Meta:
        model = Comment
        fields = ['message']


