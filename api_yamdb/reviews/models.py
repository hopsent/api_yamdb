from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager
)
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.forms import ValidationError


ROLE_CHOICES = (
    ("user", "user"),
    ("moderator", "moderator"),
    ("admin", "admin"),
)


class UserManager(BaseUserManager):
    """
    Кастомизация менеджера для :model:'reviews.User'.
    Обеспечивает регистрацию моделей без пароля.
    """

    def create_user(
        self,
        username,
        email,
        password=None,
        **kwargs,
    ):
        """
        Создание объекта :model:'reviews.User'
        с email и username - обязательными полями.
        Авторизация не предполагает наличие пароля.
        """

        if username is None:
            raise TypeError('У юзеров должен быть username.')

        if email is None:
            raise TypeError('У юзеров должен быть email.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password, **kwargs):
        """Создать суперюзера."""

        if password is None:
            raise TypeError('Суперюзер должен быть запаролен.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs,
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    """Кастомизированная модель User."""

    email = models.EmailField(
        blank=False,
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        blank=True
    )
    role = models.TextField(
        choices=ROLE_CHOICES,
        default="user"
    )

    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    def clean(self):
        """Запрет на 'me' в username."""
        super().clean()
        if self.username == 'me':
            raise ValidationError(
                "Username не может иметь значение 'me'."
            )

    def send_confirmation_code(self):
        """Отправка сообщения с кодом для получения jwt-токена."""

        confirmation_code = default_token_generator.make_token(self)
        message = f'Введите {confirmation_code} в запрос к v1/auth/token.'
        self.email_user(
            subject='Ваш confirmation_code для YaMDb.',
            message=message
        )

    # Нейтрализация предупреждения Django о некорректной работе
    # паджинации в приложении api на эндпоинте v1/users/.
    class Meta:
        ordering = ('-id',)
