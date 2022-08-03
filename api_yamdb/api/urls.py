from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register('users', views.UserViewSet)


urlpatterns = [
    path('v1/auth/signup/', views.RegistrationView.as_view()),
    path('v1/auth/token/', views.TokenObtainApiYamdbView.as_view()),
    path('v1/users/me/', views.MeUserAPIView.as_view()),
    path('v1/', include(router_v1.urls)),
]
