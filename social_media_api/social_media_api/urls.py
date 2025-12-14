from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),      # Register, Login, Follow/Unfollow
    path('api/posts/', include('posts.urls')),            # Posts CRUD + feed
    path('api/notifications/', include('notifications.urls')),  # Notifications
]
