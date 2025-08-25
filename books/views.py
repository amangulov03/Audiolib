from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.db.models import Avg
from .models import Genre, Book, ReadingProgress
from .serializers import GenreSerializer, BookSerializer, ReadingProgressSerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class IsAuthenticatedForReadAndAdminForWrite(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedForReadAndAdminForWrite]


class ReadingProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ReadingProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ReadingProgress.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedForReadAndAdminForWrite]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('genres',)
    search_fields = ('title',)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @method_decorator(cache_page(60 * 15, key_prefix="top_books")) 
    @action(detail=False, methods=['get'])
    def top(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Требуется авторизация"}, 
                status=status.HTTP_403_FORBIDDEN
            )

        books = Book.objects.annotate(
            avg_rating=Avg("reviews__rating")
        ).order_by("-avg_rating")[:10]

        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data, status=200)