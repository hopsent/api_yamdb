from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager
)

from django.db import models
from django.forms import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)

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


# Часть третьего разработчика (Дмитрий, ветка feature_3)
class Review(models.Model):
    """Отзывы на произведение."""
    title = models.ForeignKey(
        Titles,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveIntegerField(
        verbose_name='Оценка произведения',
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Оценка произведения не может быть ниже 1'
            ),
            MaxValueValidator(
                limit_value=10,
                message='Максимальная оценка не может быть выше 10'
            )
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв',
        verbose_name_plural = 'Отзывы',
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return (f'Отзыв {self.author} '
                f'на произведение {self.title}.')


class Comments(models.Model):
    """Комментарии к отзывам."""
    review = models.ForeignKey(
        Review,
        verbose_name='Ревью на произведение',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации комментария',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий',
        verbose_name_plural = 'Комментарии',
        ordering = ['pub_date']

    def __str__(self):
        return (f'Комментарий пользователя {self.author} '
                f'на отзыв {self.review}.')
