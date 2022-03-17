from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    firstname = models.CharField(
        max_length=50,
        blank=True,
    )
    lastname = models.CharField(
        max_length=50,
        blank=True,
    )
    username = models.CharField(
        verbose_name='username',
        max_length=50,
        unique=True,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name='email',
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.username
