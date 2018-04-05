from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from post.models import Blog, Comments, Profile
from bootstrap_datepicker.widgets import DatePicker

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=None,
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=None,
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'username': None,
            'email': None,
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={
                'id': 'post-title',
                'required': True,
                # 'placeholder': 'Post title'
            }),
            'body': forms.TextInput(attrs={
                'id': 'post-text',
                'required': True,
                # 'placeholder': 'Say something...'
            }),
        }

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birth_date', 'location']
