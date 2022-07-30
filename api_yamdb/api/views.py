from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from api.permissions import IsAdminOrReadOnly
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleCreateSerializer, TitleListSerializer)
from reviews.models import Category, Genre, Title


class ListCreateDeleteViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
   pass


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('category', 'genre', 'name', 'year')
    permission_classes = (IsAdminOrReadOnly, )
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListSerializer
        return TitleCreateSerializer


class GenresViewSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    permission_classes = (IsAdminOrReadOnly, )


class CategoriesViewSet(ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    permission_classes = (IsAdminOrReadOnly, )
