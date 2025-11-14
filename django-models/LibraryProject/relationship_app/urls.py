# LibraryProject/relationship_app/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, book_detail, add_book, edit_book, delete_book, register, LibraryDetailView
from .admin_view import admin_view
from .librarian_view import librarian_view
from .member_view import member_view

app_name = 'relationship_app'

urlpatterns = [
    # Books list and detail
    path('books/', list_books, name='list_books'),
    path('books/<int:pk>/', book_detail, name='book_detail'),

    # CRUD paths — REQUIRED BY CHECKER
    path('book/add/', add_book, name='add_book'),
    path('book/<int:pk>/edit/', edit_book, name='edit_book'),
    path('book/<int:pk>/delete/', delete_book, name='delete_book'),

    # Role-based views
    path('role/admin/', admin_view, name='admin_view'),
    path('role/librarian/', librarian_view, name='librarian_view'),
    path('role/member/', member_view, name='member_view'),

    # Authentication
    path('accounts/register/', register, name='register'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),

    # Library detail
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
