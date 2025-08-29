from django.urls import path
from .views import FavoriteListView, FavoriteCreateView, FavoriteDeleteView

urlpatterns = [
    path('favorite/', FavoriteListView.as_view()),     
    path('favorite/add/', FavoriteCreateView.as_view()), 
    path('favorite/delete/<int:pk>/', FavoriteDeleteView.as_view()), 
]
