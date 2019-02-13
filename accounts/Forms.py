from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from .models import User, UserManager
from jobssul.widgets.daum_address_widget import DaumAddressWidget


#회원가입폼
class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(
        label=_('Email'),
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Email address'),
                'required': 'True',
            }
        )
    )
    nickname = forms.CharField(
        label=_('Nickname'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('닉네임'),
                'required': 'True',
            }
        )
    )
    username = forms.CharField(
        label=_('Name'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('이름'),
                'required': 'True',
            }
        )
    )
    reside = forms.CharField(
        label=_('거주지'),
        required=False,
        widget=DaumAddressWidget()
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password'),
                'required': 'True',
            }
        )
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password confirmation'),
                'required': 'True',
            }
        )
    )

    class Meta:
        model = User
        # fields = ('email', 'nickname')
        fields = ('email', 'nickname', 'password1', 'password2', 'reside', 'username')

        def __init__(self):
            self.cleaned_data = None
            super(UserCreationForm, self).__init__(*args, **kargs)
            # self.fields['reside'].required=False

        def clean_password2(self):
            # 두 비밀번호 입력 일치 확인
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Passwords don't match")
            return password2

        def save(self, commit=True):
            # Save the provided password in hashed format
            user = super(UserCreationForm, self).save(commit=False)
            user.email = UserManager.normalize_email(self.cleaned_data['email'])
            user.set_password(self.cleaned_data["password1"])
            if commit:
                user.save()
            return user


class UserChangeForm(forms.ModelForm):
    # 비밀번호 변경 폼
    password = ReadOnlyPasswordHashField(
        label=_('Password')
    )

    class Meta:
        model = User
        fields = ('username', 'nickname', 'email', 'password', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput) or \
                    isinstance(field.widget, forms.Textarea) or \
                    isinstance(field.widget, forms.DateInput) or \
                    isinstance(field.widget, forms.EmailInput) or \
                    isinstance(field.widget, forms.DateTimeInput) or \
                    isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({'placeholder': field.label})

