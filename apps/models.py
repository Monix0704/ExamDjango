from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import Model, CharField, EmailField, BooleanField, DateTimeField, TextField, IntegerField, ForeignKey, CASCADE


class CustomUserManager(UserManager):
    use_in_migrations = True

def _create_user_object(self, phone_number, email,username, password, **extra_fields):
    if not phone_number:
        raise ValueError("The given phone_number must be set")
    email = self.normalize_email(email)

    user = self.model(phone_number=phone_number, email=email,username=username, **extra_fields)
    user.password = make_password(password)
    return user

def _create_user(self, phone_number, email, username, password, **extra_fields):

    user = self._create_user_object(phone_number, email,username ,password, **extra_fields)
    user.save(using=self._db)
    return user


def create_user(self, phone_number, username , email=None, password=None, **extra_fields):
    extra_fields.setdefault("is_staff", False)
    extra_fields.setdefault("is_superuser", False)
    return self._create_user(phone_number, email, password,username, **extra_fields)




def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)

    if extra_fields.get("is_staff") is not True:
        raise ValueError("Superuser must have is_staff=True.")
    if extra_fields.get("is_superuser") is not True:
        raise ValueError("Superuser must have is_superuser=True.")

    return self._create_user(phone_number, email, password, **extra_fields)


class User(AbstractUser):
    objects = CustomUserManager()
    username = CharField(max_length=255,unique=True)
    email = EmailField()
    first_name = CharField(max_length=255, default="")
    last_name = CharField(max_length=255, default="")
    password = CharField(max_length=10, default="")
    is_active = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)

class Post(Model):
    title = CharField(max_length=255)
    content = TextField(default="")
    is_published = BooleanField(default=False)
    views = IntegerField(default=0)
    user_id = ForeignKey("User", on_delete=CASCADE,related_name="posts")
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

class Comment(Model):
    content = CharField(max_length=255)
    user_id = ForeignKey("User", on_delete=CASCADE,related_name="comments")
    post_id = ForeignKey("Post", on_delete=CASCADE,related_name="comments")
    created_at = DateTimeField(auto_now_add=True)

