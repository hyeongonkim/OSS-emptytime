from django import forms
from .models import User

class PostForm(forms.ModelForm):
    username_text = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'input100', 'name': 'studentid'}
        )
    )
    pw_text = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'input100', 'name': 'pass'}
        )
    )
    class Meta:
        model = User
        fields = ('username_text', 'pw_text',)