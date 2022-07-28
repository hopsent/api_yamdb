from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('auth/signup', views.RegistrationViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
