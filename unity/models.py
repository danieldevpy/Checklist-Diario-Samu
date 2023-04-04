from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from categorias.models import Unidade

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(email=email, password=password, **extra_fields)



class User(AbstractUser):
    username = models.CharField(max_length=45, unique=True)
    unity = models.ForeignKey(Unidade, null=True, on_delete=models.SET_NULL)
    usa = models.BooleanField(default=True, verbose_name='USA')
    usb = models.BooleanField(default=True, verbose_name='USB')
    objects = CustomUserManager()

    USERNAME_FIELD = "username"


    def __str__(self):
        return self.username