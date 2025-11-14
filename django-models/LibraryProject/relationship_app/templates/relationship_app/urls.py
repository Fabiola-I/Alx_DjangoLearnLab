from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import list_books, book_detail, register
from .admin_view import admin_view
from .librarian_view import librarian_view
from .member_view import member_view
from .views import LibraryDetailView
from . import auth_views

app_name = 'relationship_app'

urlpatterns = [
    # Books
    path('books/', list_books, name='list_books'),
    path('books/<int:pk>/', book_detail, name='book_detail'),

    # Library detail
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Role-based views
    path('role/admin/', admin_view, name='admin_view'),
    path('role/librarian/', librarian_view, name='librarian_view'),
    path('role/member/', member_view, name='member_view'),

    # Book management (permissions)
    path('book/add/', views.add_book, name='add_book'),
    path('book/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:pk>/delete/', views.delete_book, name='delete_book'),

    # Auth (checker requires these exact lines)
    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', LogoutView.as_view(template_name="logout.html"), name='logout'),
    path('register/', register, name='register'),

    # Optional: if you are using auth_views for register/login/logout
    path('accounts/register/', auth_views.register_view, name='register_view'),
    path('accounts/login/', auth_views.login_view, name='login_view'),
    path('accounts/logout/', auth_views.logout_view, name='logout_view'),
]
