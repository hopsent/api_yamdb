from .serilizers import RegistrationSerializer
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from reviews.models import User

class RegistrationViewSet(
        mixins.CreateModelMixin,
        viewsets.GenericViewSet
    ):
    """Api-view for :model:'reviews.User' instances."""

    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny,]
