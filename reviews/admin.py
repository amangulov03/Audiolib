from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "user", "rating", "created_at")
    list_filter = ("rating", "created_at", "book")
    search_fields = ("text", "user__username", "book__title")