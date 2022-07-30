from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import TitlesViewSet, GenresViewSet, CategoriesViewSet

router_1 = DefaultRouter()
router_1.register('titles', TitlesViewSet, basename='title')
router_1.register('genres', GenresViewSet, basename='genre')
router_1.register('categories', CategoriesViewSet, basename='category')
urlpatterns = [
    path('', include(router_1.urls))
]