from turtle import title
from rest_framework import serializers

from reviews.models import User, Review, Comments


class RegistrationSerializer(serializers.ModelSerializer):
    """Sign up serialization."""

    class Meta:
        model = User
        fields = ('email', 'username')


# Часть третьего разработчика (Дмитрий, ветка feature_3)
class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация отзывов."""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        # на счёт параметра default я плохо понял
        # если пайтест не пройдёт, то попробовать
        # его разкомментить
        # default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title', 'author'],
                message='Отзыв на произведение уже есть'
            )
        ]

    def validate(self, data):
        if data['title'] == data['author']:
            raise serializers.ValidationError(
                'Повторно оставить отзыв на произведение невозможно'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация комментариев."""
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comments
        fields = '__all__'
