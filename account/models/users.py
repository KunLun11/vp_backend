from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from account.managers.users import UserManager
from config.core.enums.users import UserRole
from etc.models.bases import UUIDTimeBaseModel


class User(UUIDTimeBaseModel, AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    username = None
    first_name = None
    last_name = None

    email = models.EmailField("Email", unique=True)
    phone = PhoneNumberField("Номер телефона", unique=True)
    phone_activated = models.BooleanField("Номер телефона активирован", default=True, blank=True)
    is_verified = models.BooleanField("Подтвержден", default=False)
    last_login_at = models.DateTimeField("Последний вход в", null=True, blank=True)
    role = models.CharField(
        "Роль",
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.player,
    )

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ()

    def __str__(self):
        return self.email
