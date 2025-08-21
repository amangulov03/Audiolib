from django.contrib import admin
from .models import Genre, Book

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'format_type')
    filter_horizontal = ('genres',)