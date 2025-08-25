from rest_framework import serializers
from .models import Genre, Book, ReadingProgress
from reviews.serializers import ReviewSerializer

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']

class ReadingProgressSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_author = serializers.CharField(source='book.author', read_only=True)
    
    class Meta:
        model = ReadingProgress
        fields = [
            'id', 'book', 'book_title', 'book_author', 
            'last_position', 'last_timecode', 'last_page', 
            'updated_at', 'completion_percentage'
        ]
        read_only_fields = ['user', 'updated_at', 'completion_percentage']

class BookListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка книг"""
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'published_date', 
            'format_type', 'cover_image', 'genres', 'average_rating'
        ]
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return 0
        total_rating = sum(review.rating for review in reviews)
        return round(total_rating / len(reviews), 2)

class BookDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для одной книги"""
    genres = GenreSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    reading_progress = serializers.SerializerMethodField()
    is_in_user_library = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'description', 'published_date', 
            'format_type', 'file', 'cover_image', 'total_pages', 'duration',
            'genres', 'reviews', 'average_rating', 'reading_progress',
            'is_in_user_library', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return 0
        total_rating = sum(review.rating for review in reviews)
        return round(total_rating / len(reviews), 2)
    
    def get_reading_progress(self, obj):
        """Получение прогресса чтения для текущего пользователя"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                progress = ReadingProgress.objects.get(
                    user=request.user, 
                    book=obj
                )
                return ReadingProgressSerializer(progress).data
            except ReadingProgress.DoesNotExist:
                return None
        return None
    
    def get_is_in_user_library(self, obj):
        """Проверка, есть ли книга в библиотеке пользователя"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ReadingProgress.objects.filter(
                user=request.user, 
                book=obj
            ).exists()
        return False

# Основной сериализатор (можно использовать context для определения поведения)
class BookSerializer(serializers.ModelSerializer):
    """Умный сериализатор, который адаптируется под контекст"""
    genres = GenreSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'description', 
            'published_date', 'format_type', 'file', 
            'cover_image', 'genres', 'average_rating'
        ]
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return 0
        total_rating = sum(review.rating for review in reviews)
        return round(total_rating / len(reviews), 2)
    
    def to_representation(self, instance):
        """Динамическое изменение output в зависимости от контекста"""
        request = self.context.get('request')
        
        if request and 'detail' in request.query_params:
            # Для детального просмотра используем полную версию
            return BookDetailSerializer(instance, context=self.context).to_representation(instance)
        else:
            # Для списка используем упрощенную версию
            representation = super().to_representation(instance)
            # Добавляем reviews только если явно запрошено
            if request and 'with_reviews' in request.query_params:
                representation['reviews'] = ReviewSerializer(
                    instance.reviews.all(), 
                    many=True
                ).data
            return representation