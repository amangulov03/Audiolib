from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsAuthorOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(book_id=self.kwargs["book_id"])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, book_id=self.kwargs["book_id"])
