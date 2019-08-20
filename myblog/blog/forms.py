from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment


# class UserForm(forms.ModelForm):
#    password = forms.CharField(widget=forms.PasswordInput())
#
#    class Meta:
#        model = User
#        fields = ('username', 'email', 'password')


class UserForm2(UserCreationForm):
    # password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# class UserProfileInfoForm(forms.ModelForm):
#    class Meta:
#        model = UserProfileInfo
#        fields = ('portfolio_site', 'profile_pic')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'title', 'text')
        # adding widgets
        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            # postcontent is our custom class
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')
        # adding widgets
        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            # postcontent is our custom class
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'})
        }
