from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, GenreViewSet, ReadingProgressViewSet
from reviews.views import ReviewViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'reading-progress', ReadingProgressViewSet, basename='readingprogress')

urlpatterns = [
    path('', include(router.urls)),
    path('books/<int:book_id>/reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='book-reviews'),
    path('books/<int:book_id>/reviews/<int:pk>/', ReviewViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='book-review-detail'),
]