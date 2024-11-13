from django.db import models
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.core.validators import RegexValidator


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

    class StatusChoices(models.TextChoices):
        NEW = "new", "New"
        CODE_VERIFIED = "code_verified", "Code Verified"

    phone_validator = RegexValidator(
        regex=r'^\+998[0-9]{9}$',
        message="Telefon raqami noto‘g‘ri formatda. Telefon raqami +998 bilan boshlanishi va 9 ta raqamdan iborat bo‘lishi kerak."
    )

    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[phone_validator]
    )
    status = models.CharField(max_length=255, choices=StatusChoices.choices, default=StatusChoices.NEW)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    def save(self, *args, **kwargs):
        if self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)