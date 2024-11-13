from django.db import models
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.core.validators import RegexValidator
import re
from rest_framework.exceptions import ValidationError

def validate_phone(value):
    phone_regex = re.compile(r'^\+998\d{9}$')
    if not phone_regex.match(value):
        raise ValidationError({"phone": "Phone is not valid"})


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
        extra_fields.setdefault('status', 'code_verified')

        return self.create_user(phone, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    last_name = None
    email = None

    class StatusChoices(models.TextChoices):
        NEW = "new", "New"
        CODE_VERIFIED = "code_verified", "Code Verified"

    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[validate_phone]
    )
    status = models.CharField(max_length=255, choices=StatusChoices.choices, default=StatusChoices.NEW)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    def save(self, *args, **kwargs):
        if not self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)