from rest_framework import serializers
from .models import Genre, Book
from reviews.serializers import ReviewSerializer

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']

class BookSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'description', 
            'published_date', 'format_type', 'file', 
            'cover_image', 'genres', "reviews",
            "average_rating"
        ]

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        total_reviews = len(reviews)
        if total_reviews == 0:
            return 0
        total_rating = sum([review.rating for review in reviews])
        average = total_rating / total_reviews
        return round(average, 2)