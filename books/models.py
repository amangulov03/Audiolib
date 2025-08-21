from django.db import models

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

# Create your models here.
