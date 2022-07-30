import datetime

from rest_framework import serializers
from reviews.models import Category, Genre, Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id', )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id', )

        
class TitleListSerializer(serializers.ModelSerializer):
    category= CategorySerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = '__all__'
    
    def validate(self, data):
        if data['year'] > datetime.date.today().year:
            message = 'Год выпуска не может быть больше текущего'
            raise serializers.ValidationError(message)
        return data


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug', queryset=Genre.objects.all(), many=True)
    description = serializers.CharField(required=False)

    class Meta:
        exclude = ('rating',)
        model = Title

    def validate(self, data):
        if data['year'] > datetime.date.today().year:
            message = 'Год выпуска не может быть больше текущего'
            raise serializers.ValidationError(message)
        return data


