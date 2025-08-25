from django.db import models
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User 

FORMAT_CHOICES = [
    ('ebook', 'Электронная книга (PDF/EPUB)'),
    ('audio', 'Аудиокнига (MP3)'),
]

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    format_type = models.CharField(
        max_length=10,
        choices=FORMAT_CHOICES,
        default='ebook'
    )
    file = models.FileField(upload_to="books/", blank=True, null=True)
    cover_image = models.ImageField(upload_to="covers/", blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name="books")

    def __str__(self):
        return f"{self.title} ({self.get_format_type_display()})"
    
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class ReadingProgress(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reading_progress')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_progress')
    last_position = models.FloatField(default=0.0, verbose_name="Последняя позиция (%)")
    last_timecode = models.CharField(max_length=20, blank=True, verbose_name="Временная метка")
    last_page = models.IntegerField(default=0, verbose_name="Последняя страница")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        unique_together = ['user', 'book']  # Одна запись на пользователя и книгу
        verbose_name = 'Прогресс чтения'
        verbose_name_plural = 'Прогресс чтения'

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.last_position}%"