from rest_framework import serializers

from reviews.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Sign up serialization."""

    class Meta:
        model = User
        fields = ('email', 'username')
