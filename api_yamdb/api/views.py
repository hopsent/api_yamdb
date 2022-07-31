from django.shortcuts import get_object_or_404
from .serilizers import (
    RegistrationSerializer,
    ReviewSerializer,
    CommentSerializer
)
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from reviews.models import (
    User,
    Review,
)


class RegistrationViewSet(
        mixins.CreateModelMixin,
        viewsets.GenericViewSet
    ):
    """Api-view for :model:'reviews.User' instances."""

    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny,]


# Часть третьего разработчика (Дмитрий, ветка feature_3)
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
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
    serializer_class = CommentSerializer
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
