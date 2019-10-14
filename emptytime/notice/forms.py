from django.forms import ModelForm
from django import forms
from .models import Mytag
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'input100', 'name': 'id'}
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={'class': 'input100', 'name': 'pass'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'input100', 'name': 'pass'}
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class LoginForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'input100', 'name': 'id'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'input100', 'name': 'pass'}
        )
    )

    class Meta:
        model = User
        fields = ('username', 'password',)

# class EmailForm(ModelForm):
#     class Meta:
#         model = EmailAccount
#         fields = ['myEmail']
#         labels = {
#             'myEmail': _('이메일 입력'),
#         }
#         help_texts = {
#             'myEmail': _('이메일을 입력해주세요.'),
#         }
#
#         error_messages = {
#             'name': {
#                 'max_length': _("이메일이 너무 깁니다. 30자 이하로 해주세요."),
#             },
#         }

class TagForm(ModelForm):
    myTag = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'input100', 'name': 'tag'}
        )
    )

    class Meta:
        model = User
        fields = ('myTag',)
