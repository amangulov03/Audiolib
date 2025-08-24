from rest_framework import viewsets
from .models import Genre, Book
from .serializers import GenreSerializer, BookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.db.models import Avg
from rest_framework.decorators import action
from rest_framework.response import Response



class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('genres',)
    search_fields = ('title', )

    @action(detail=False, methods=['get'])
    def top(self, request):
        books = Book.objects.annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('-avg_rating')[:10]

        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data, status=201)
