from django.urls import path
from . import views
from .admin_view import admin_view
from .librarian_view import librarian_view
from .member_view import member_view
from .views import LibraryDetailView
from . import auth_views
app_name = 'relationship_app'

urlpatterns = [
    path('books/', views.list_books, name='list_books'),            # function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # class-based view

    # role-based views
    path('role/admin/', admin_view, name='admin_view'),
    path('role/librarian/', librarian_view, name='librarian_view'),
    path('role/member/', member_view, name='member_view'),

    # book management (permissions)
    path('book/add/', views.add_book, name='add_book'),
    path('book/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:pk>/delete/', views.delete_book, name='delete_book'),
    path('accounts/register/', auth_views.register_view, name='register'),
    path('accounts/login/', auth_views.login_view, name='login'),
    path('accounts/logout/', auth_views.logout_view, name='logout'),
]
