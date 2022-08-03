from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
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
    path('v1/auth/signup/', views.RegistrationView.as_view()),
    path('v1/auth/token/', views.TokenObtainApiYamdbView.as_view()),
    path('v1/users/me/', views.MeUserAPIView.as_view()),
    path('v1/', include(router.urls)),
]
