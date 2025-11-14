from django.urls import path
from . import views
from .admin_view import admin_view
from .librarian_view import librarian_view
from .member_view import member_view

app_name = 'relationship_app'

urlpatterns = [
    path('role/admin/', admin_view, name='admin_view'),
    path('role/librarian/', librarian_view, name='librarian_view'),
    path('role/member/', member_view, name='member_view'),
]
