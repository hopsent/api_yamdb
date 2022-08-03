from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase

from . import serilizers as s
from .permissions import AdminOnly, SelfOnly
from reviews.models import User, Review


class UserViewSet(viewsets.ModelViewSet):
    """
    Отображает, создает, обновляет и удаляет
    инстансы, относящиеся к :model:'posts.Post'.
    Представление доступно только юзерам с ролью
    'admin' и суперюзеру. Настроен поиск по полю
    'username'. При обращении к detail-представлению
    используется слаг 'username'.
    """

    queryset = User.objects.all()
    serializer_class = s.UserSerializer
    permission_classes = [AdminOnly, ]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'


class MeUserAPIView(APIView):
    """
    На эндпоинте v1/users/me предусматриваем представление
    объекта :model:'reviews.User', который можно либо
    получить (просмотреть), либо частично обновить.
    Эндпоинт доступен только авторизованным (jwt-токен)
    юзерам-объектам запроса.
    """

    permission_classes = [SelfOnly, ]

    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = s.MeUserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = s.MeUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class RegistrationView(APIView):
    """
    Api-view для регистрации :model:'reviews.User' объектов.
    Любой допущен к регистрации таких инстансов.
    Также отправляет confirmation_code для получения jwt-токена.
    Поля - 'username' и 'email'.
    """

    permission_classes = [AllowAny, ]

    def post(self, request):
        """"Обработка POST-запроса на эндпоинт v1/auth/signup."""
        serializer = s.RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # При создании нового юзера направляем конфирмационный код.
            username = serializer.data['username']
            user = get_object_or_404(User, username=username)
            user.send_confirmation_code()
            return Response(serializer.data, status=status.HTTP_200_OK)
        # При пост-запросе отправка кода на email
        # существующему юзеру проводится на initial_data,
        # поскольку данные не прошли валидацию.
        try:
            username = serializer.initial_data['username']
            email = serializer.initial_data['email']
            if User.objects.filter(username=username, email=email).exists():
                user = User.objects.get(username=username, email=email)
                user.send_confirmation_code()
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        # Перехватываем ошибки отсутствия 'username' и 'email',
        # поскольку метод .is_valid() не предусматривает выбрасывание
        # exception по причине необходимости направления электронного письма
        # даже в случае ошибки валидации.
        except KeyError or ValidationError:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class TokenObtainApiYamdbView(TokenViewBase):
    """
    Вью-класс для эндпоинта v1/auth/token.
    Предназначен для выдачи jwt-токена.
    По сравнению с базовым: переопределен сериализатор.
    Введена настройка доступа - "для всех" - отличная
    от настроек проекта в settings.py.
    """

    permission_classes = (AllowAny,)
    serializer_class = s.YAMDbTokenObtainSerializer


# Часть третьего разработчика (Дмитрий, ветка feature_3)
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = s.ReviewSerializer
    # пермишены ещё не написаны
    # следую названиям как учили в теории
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        author = self.request.user
        serializer.save(title=title, author=author)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = s.CommentSerializer
    # пермишены ещё не написаны
    # следую названиям как учили в теории
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title=title_id)
        author = self.request.user
        serializer.save(review=review, author=author)
