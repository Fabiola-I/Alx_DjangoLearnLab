from django.contrib import admin
from django.urls import path, include  # include is needed if you have app urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),  # example app urls
    path('accounts/', include('accounts.urls')), # optional, if you create app urls
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
