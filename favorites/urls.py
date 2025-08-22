from django.urls import path
from .views import FavoriteListView, FavoriteCreateView, FavoriteDeleteView

urlpatterns = [
    path('favorite/', FavoriteListView.as_view()),     
    path('favorite/add/', FavoriteCreateView.as_view()), 
    path('favorite/<int:pk>/delete/', FavoriteDeleteView.as_view()), 
]
