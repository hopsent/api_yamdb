from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager
)

from django.db import models
from django.forms import ValidationError


ROLE_CHOICES = [
    ("user", "user"),
    ("moderator", "moderator"),
    ("admin", "admin"),
]


class UserManager(BaseUserManager):
    """
    Customized :model:'reviews.User' management.
    Providing password-free creating objects.
    """

    def create_user(self, username, email, password=None):
        """
        Creating an instance of :model:'reviews.User' 
        with email and username. Django set password field
        as required. That's why we shall set
        each user's password as None.
        """

        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
                raise TypeError(
                    'Users must have an email address.'
                )

        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
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
        if self.username == 'me':
            raise ValidationError(
                "Username не может иметь значение 'me'."
            )
