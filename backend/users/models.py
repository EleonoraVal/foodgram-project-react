from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
ADMIN = 'admin'

CHOICES = (
    (USER, 'пользователь'),
    (ADMIN, 'администратор')
)


class User(AbstractUser):
    first_name = models.CharField(
        max_length=50,
        blank=True,
    )
    last_name = models.CharField(
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
    role = models.CharField(
        verbose_name='статус',
        max_length=50,
        choices=CHOICES,
        default=USER,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', ],
                name='unique_username'
            ),
            models.UniqueConstraint(
                fields=['email', ],
                name='unique_email'
            )
        ]

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == USER

    def __str__(self):
        return self.username
