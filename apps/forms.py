from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, CharField
from apps.models import User


class LoginForm(Form):
    username = CharField(max_length=50)
    password = CharField(max_length=10)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        queryset = User.objects.filter(username=username)
        if not queryset.exists():
            raise ValidationError("Account topilmadi")
        user = queryset.first()
        if not check_password(password, user.password):
            raise ValidationError("Password notogri")
        self.session_user = user
        return super().clean()

