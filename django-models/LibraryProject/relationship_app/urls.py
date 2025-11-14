# LibraryProject/relationship_app/urls.py
from django.urls import path
from .views import list_books, book_detail, register
from django.contrib.auth.views import LoginView, LogoutView
from .admin_view import admin_view
from .librarian_view import librarian_view
from .member_view import member_view
from .views import LibraryDetailView
from django.urls import path
from . import views
app_name = 'relationship_app'

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('books/<int:pk>/', book_detail, name='book_detail'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
     path('register/', views.register, name='register'),    # Role-based views
    path('role/admin/', admin_view, name='admin_view'),
    path('role/librarian/', librarian_view, name='librarian_view'),
    path('role/member/', member_view, name='member_view'),

    # Book management
    path('book/add/', list_books, name='add_book'),  # adjust if you have add_book view
    path('book/<int:pk>/edit/', list_books, name='edit_book'),  # adjust accordingly
    path('book/<int:pk>/delete/', list_books, name='delete_book'),  # adjust accordingly

    # Authentication
    path('accounts/register/', register, name='register'),  # <--- THIS IS REQUIRED
    path('accounts/login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('accounts/logout/', LogoutView.as_view(template_name="logout.html"), name='logout'),
]
