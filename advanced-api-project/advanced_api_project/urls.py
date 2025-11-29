from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Required by checker
    path('api/', include('api.urls')),
]
