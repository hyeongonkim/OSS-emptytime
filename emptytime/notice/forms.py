from django.forms import ModelForm
from django import forms
from .models import Mytag
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email', 'password']
        labels = {
            'username': _('ID'),
        }
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
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
    class Meta:
        model = Mytag
        fields = ['account','myTag']
        widgets = {
            'account': forms.HiddenInput(),  # 어떤 계정에 저장하는지 숨김

        }
        labels = {
            'account': _('ID입력'),
            'myTag': _('태그 입력'),
        }
        help_texts = {
            'account': _('ID를 입력해주세요'),
            'myTag': _('태그를 입력해주세요.'),
        }

        error_messages = {
            'name': {
                'max_length': _("태그가 너무 깁니다. 20자 이하로 해주세요."),
            },
        }
