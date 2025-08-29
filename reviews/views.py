from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework.exceptions import ValidationError

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        book_id = self.kwargs.get("book_id")
        if book_id:  # вложенный урл
            return Review.objects.filter(book_id=book_id)
        return Review.objects.all()  # для /reviews/<pk>/

    def perform_create(self, serializer):
        book_id = self.kwargs.get("book_id")
        if not book_id:
            raise ValidationError("Нельзя создать отзыв без указания книги")
        serializer.save(user=self.request.user, book_id=book_id)
