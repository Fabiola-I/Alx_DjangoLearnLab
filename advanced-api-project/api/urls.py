# api/urls.py
from django.urls import path
from .views import (
    BookListCreateView, BookDetailView,
    AuthorListCreateView, AuthorDetailView
)

urlpatterns = [
    # Book endpoints
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    # Author endpoints
    path('authors/', AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
]
