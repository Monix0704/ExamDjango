from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.db.models import Q

from apps.models import User, Post, Comment


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    username = forms.CharField(max_length=300)
    email = forms.EmailField(max_length=300)
    password = forms.PasswordInput()
    password2 = forms.PasswordInput()

    def clean(self):
        cleaned_data = super().clean()

        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        query = User.objects.filter(
            Q(username=username) | Q(email=email)
        )
        if query.exists():
            ValidationError('User already exists')

        if password2 != password:
            ValidationError('Passwords do not match')

        if len(str(password)) < 8:
            ValidationError('Password should contain at least 8 characters')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password
        )

        cleaned_data['user'] = user
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username or not password:
            return cleaned_data

        user = User.objects.filter(username=username)

        if not user.exists():
            raise ValidationError("User doesn't exist'")

        user = user.first()

        if not check_password(password, user.password):
            raise ValidationError("Invalid credentials")

        cleaned_data['user'] = user

        return cleaned_data


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'is_published',
        ]

    def save(self, commit = True):
        post = super().save(commit=False)

        title = self.cleaned_data.get('title')
        content = self.cleaned_data.get('content')

        if not title or not content:
            ValidationError('Title or Content is missing')


        if commit:
            post.save()

        return post

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]
