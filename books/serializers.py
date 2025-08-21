from rest_framework import serializers
from .models import Genre, Book

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']

class BookSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'description', 
            'published_date', 'format_type', 'file', 
            'cover_image', 'genres'
        ]