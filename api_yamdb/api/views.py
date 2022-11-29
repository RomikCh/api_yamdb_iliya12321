from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from reviews.models import Review, Title
from api.serializers import CommentSerializer, ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = 'потом'

    def _get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self._get_review().comments

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self._get_review())


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = 'потом'

    def _get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self._get_title().reviews

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self._get_title())
