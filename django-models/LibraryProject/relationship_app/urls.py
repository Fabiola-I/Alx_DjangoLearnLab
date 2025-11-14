# django-models/LibraryProject/relationship_app/urls.py (FINAL COMPLETE)

from django.urls import path
from . import views
from .views import LibraryDetailView
from django.contrib.auth import views as auth_views 

urlpatterns = [
    # --- Task 1 URLs ---
    path('books/', views.book_list, name='book_list'), 
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # --- Task 2: User Authentication URLs ---
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register_view, name='register'),

    # --- Task 3: Role-Based Access Control URLs ---
    path('admin_area/', views.admin_view, name='admin_view'),
    path('librarian_desk/', views.librarian_view, name='librarian_desk'),
    path('member_dashboard/', views.member_view, name='member_dashboard'),
    
    # --- Task 4: Custom Permissions URLs (STRICT CHECK FIX) ---
    
    # 1. Adds 'add_book/' to the path string
    path('books/add_book/', views.book_add_view, name='book_add'),
    
    # 2. Adds 'edit_book/' to the path string, keeping the primary key (<int:pk>)
    path('books/edit_book/<int:pk>/', views.book_edit_view, name='book_edit'),
    
    # 3. Adds 'delete_book/' to the path string, keeping the primary key (<int:pk>)
    path('books/delete_book/<int:pk>/', views.book_delete_view, name='book_delete'),
]