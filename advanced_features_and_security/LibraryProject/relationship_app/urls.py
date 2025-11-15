# relationship_app/urls.py

from django.urls import path
from . import views
from .admin_view import admin_view
from .librarian_view import librarian_view
from .member_view import member_view
from .views import LibraryDetailView

app_name = 'relationship_app'

urlpatterns = [
    # ------------------------------
    # Book-related paths
    # ------------------------------
    path('books/', views.list_books, name='list_books'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),

    # CRUD operations
    path('book/add/', views.add_book, name='add_book'),
    path('book/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:pk>/delete/', views.delete_book, name='delete_book'),

    # ------------------------------
    # Role-based views
    # ------------------------------
    path('role/admin/', admin_view, name='admin_view'),
    path('role/librarian/', librarian_view, name='librarian_view'),
    path('role/member/', member_view, name='member_view'),

    # ------------------------------
    # Library detail view
    # ------------------------------
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # ------------------------------
    # Authentication paths
    # ------------------------------
    # ⚠️ Only keep registration here if custom; login/logout handled by two_factor
    path('accounts/register/', views.register, name='register'),
]
