from django.db import models
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Telefon raqami kiritilishi kerak')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    last_name = None
    email = None
    phone = models.CharField(max_length=15, unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone