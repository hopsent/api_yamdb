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
    Customized :model:'reviews.User' management.
    Providing password-free creating objects.
    """

    def create_user(
        self,
        username,
        email,
        role,
        password=None,
        **kwargs,
    ):
        """
        Creating an instance of :model:'reviews.User'
        with email and username. Django set password field
        as required. That's why we shall set
        each user's password as None.
        """

        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs
        )
        if role == 'admin':
            user.is_staff = True
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password, **kwargs):
        """
        Creating superuser.
        """

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    """Customized User model."""

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

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def clean(self):
        """Setting 'me' as prohibited username."""
        super().clean()
        if self.username == 'me':
            raise ValidationError(
                "Username не может иметь значение 'me'."
            )

    def send_confirmation_code(self):
        """
        Sending email with confirmation_code.
        This code's required to get jwt-token.
        """

        confirmation_code = default_token_generator.make_token(self)
        message = f'Введите {confirmation_code} в запрос к api/v1/auth/token'
        self.email_user(
            subject="It's your confirmation code for YaMDb.",
            message=message
        )
