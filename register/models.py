from django.contrib.auth.models import AbstractUser
from django.db import models


class Customer(AbstractUser):
    class UserRole(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    role = models.TextField('Роль', choices=UserRole.choices,
                            default=UserRole.USER, )

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
