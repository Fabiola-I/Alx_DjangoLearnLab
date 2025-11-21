from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),

    # Token retrieval endpoint (use username & password to get a token)
    path('api/api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # include the api app URLs under /api/
    path('api/', include('api.urls')),
]
