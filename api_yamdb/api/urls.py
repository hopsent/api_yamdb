from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('auth/signup', views.RegistrationViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
    r'/comments',
    views.CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/', include(router.urls)),
]
