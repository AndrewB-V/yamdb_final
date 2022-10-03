from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **fields):
        if email is None:
            raise TypeError('Укажите email')

        if username is None:
            raise TypeError('Укажите username')

        if username == 'me':
            raise ValueError(
                'Имя (me) в качестве username запрещено.'
            )

        user = self.model(
            username=username, email=self.normalize_email(email), **fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password, **fields):
        if password is None:
            raise TypeError('Укажите пароль')

        user = self.create_user(username, email, password, **fields)
        user.is_superuser = True
        user.is_staff = True
        user.role = 'admin'
        user.save()

        return user


class User(AbstractUser):
    ROLES = [('user', 'user'),
             ('moderator', 'moderator'),
             ('admin', 'admin')]

    username = models.CharField(
        max_length=150,
        unique=True
    )

    email = models.EmailField(
        'Почта',
        unique=True
    )

    bio = models.TextField(
        'Биография',
        blank=True
    )

    role = models.CharField(
        'Роль',
        max_length=10,
        choices=ROLES,
        default='user'
    )

    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_auth'
            ),
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
