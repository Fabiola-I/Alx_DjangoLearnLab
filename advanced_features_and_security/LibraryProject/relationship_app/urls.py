# File: LibraryProject/urls.py

from django.contrib import admin
from django.urls import path, include
# You might need to import your custom views if you have a homepage view here
# from . import views 

urlpatterns = [
    # Django Admin path
    path('admin/', admin.site.urls),
    
    # ⭐ FIX 1: Include the two_factor URLs with the correct namespace
    # The login path 'accounts/login/' or just '' often uses this inclusion.
    path('accounts/', include('two_factor.urls', 'two_factor')),
    
    # Include your application's URLs
    path('', include('relationship_app.urls')),
    
    # Optional: A path for a generic homepage if you need one
    # path('', views.home_view, name='home'),
]