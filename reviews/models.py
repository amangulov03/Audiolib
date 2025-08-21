from django.db import models
from django.contrib.auth import get_user_model

from books.models import Book

User = get_user_model()

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField("Отзыв")
    rating = models.PositiveIntegerField("Оценка", choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ("book", "user")

    def __str__(self): 
        return f"Отзыв {self.user} на {self.book} — {self.rating}/5"
