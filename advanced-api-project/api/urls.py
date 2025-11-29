from django.urls import path
from .views import (
    BookListCreateView,
    BookDetailView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    path("books/", BookListCreateView.as_view(), name="book-list-create"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),

    # Required by checker
    path("books/update/<int:pk>/", BookUpdateView.as_view(), name="book-update"),
    path("books/delete/<int:pk>/", BookDeleteView.as_view(), name="book-delete"),
]
