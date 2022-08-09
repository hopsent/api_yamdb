from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import User, Review, Comments, Category, Genre, Title


class UserSerializer(serializers.ModelSerializer):
    """
    Общий сериализатор для :model:'reviews.Users'.
    Не предусматривает специальных настроек,
    потому что предназначен к использованию
    исключительно администрацией сайта, как это
    предусмотрено в соответствующем представлении.
    """

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'bio',
            'role',
            'first_name',
            'last_name'
        )


class MeUserSerializer(serializers.ModelSerializer):
    """
    Сериализация detail-представления для инстанса,
    относящегося к :model:'reviews.Users'.
    На уровне представления позволяет читать и патчить
    существующие инстансы, кроме поля 'role', чтобы
    юзер не смог сделать себя админом сайта и получить
    дополнительные пермишены.
    """

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'bio',
            'role',
            'first_name',
            'last_name'
        )
        read_only_fields = ['role']


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализация для регистрации новых инстансов,
    относящихся к :model:'reviews.User'.
    Валидация предполагает исключение текста 'me'
    из поля 'username', поскольку иное нарушит
    url-схему проекту.
    """

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя назвать юзера "me".'
            )
        return value


class YAMDbTokenObtainSerializer(serializers.Serializer):
    """
    Сериализатор для выдачи токенов по запросу
    на эндпоинт v1/auth/token.
    Переопределены поля: вместо 'password' используется
    'confirmation_code' - дефолтный токен Джанго, направленный
    юзеру по запросу к эндпоинту v1/auth/signup/.
    Респонз - это аксесс-токен (рефреш-токен не выдается).
    """

    token = AccessToken
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    # Далее валидируем поля на наличие данных.
    def validate_confirmation_code_field(self, value):
        if not value:
            raise ValidationError(
                {'confirmation_code':
                    'Поле confirmation_code не может быть пустым.'}
            )
        return value

    def validate_username_field(self, value):
        if not value:
            return ValidationError(
                {'username': 'Поле username не может быть пустым.'}
            )
        return value

    def validate(self, attrs):
        token = attrs['confirmation_code']
        # Проверяем наличие юзера с запрошенным 'username' в базе.
        if not User.objects.filter(username=attrs['username']).exists():
            raise NotFound(
                {'username': 'Юзер с таким username отсутствует в базе.'}
            )
        user = User.objects.get(username=attrs['username'])
        # Проверка правильности введенного в поле 'confirmation_code'
        # дефолтного токена Django.
        if not default_token_generator.check_token(user=user, token=token):
            raise ValidationError(
                {'confirmation_code':
                    'Введен не присвоенный юзеру confirmation_code.'}
            )
        # Далее излагается логика сериализатора-родителя
        # с поправкой на кастомные поля.
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "confirmation_code": attrs["confirmation_code"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)
        # Возвращаем аксесс-токен как словарь 'data'.
        data = {}
        data["access"] = str(self.token.for_user(user))

        return data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        if request.method == 'POST':
            if Review.objects.filter(title=title_id, author=author).exists():
                raise serializers.ValidationError(
                    'Вы не можете добавить более'
                    'одного отзыва на произведение'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация комментариев."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор для жанров.
    """

    class Meta:
        model = Genre
        exclude = ('id', )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id', )


class TitleListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления списка Titles.
    """

    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания Title.
    """
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    description = serializers.CharField(required=False)

    class Meta:
        exclude = ('rating',)
        model = Title

    def validate(self, data):
        try:
            data['year']
        except KeyError:
            print('Необходимо указать год')
        return data
