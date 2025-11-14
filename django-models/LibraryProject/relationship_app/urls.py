# LibraryProject/relationship_app/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # Import views as a module
from .admin_view import admin_view
from .librarian_view import librarian_view
from .member_view import member_view
from .views import LibraryDetailView

app_name = 'relationship_app'

urlpatterns = [
    # Books list and detail
    path('books/', views.list_books, name='list_books'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),

    # CRUD paths
    path('book/add/', views.add_book, name='add_book'),
    path('book/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:pk>/delete/', views.delete_book, name='delete_book'),

    # Role-based views
    path('role/admin/', admin_view, name='admin_view'),
    path('role/librarian/', librarian_view, name='librarian_view'),
    path('role/member/', member_view, name='member_view'),

    # Authentication
    path('accounts/register/', views.register, name='register'),  # <-- uses views.register now
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    # Add these lines inside your urlpatterns in urls.py
    path('book/add/', views.add_book, name='add_book'),       # contains "add_book/"
    path('book/<int:pk>/edit/', views.edit_book, name='edit_book'),  # contains "edit_book/"
    # Library detail
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
