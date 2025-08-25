from django.contrib import admin
from .models import Genre, Book, ReadingProgress

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'format_type')
    filter_horizontal = ('genres',)

@admin.register(ReadingProgress)
class ReadingProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'last_position', 'last_page', 'updated_at')
    list_filter = ('book', 'user')
    search_fields = ('user__username', 'book__title')