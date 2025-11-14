# in django-models/urls.py (project)
from django.urls import path, include

urlpatterns = [
    # ... other patterns ...
    path('', include('relationship_app.urls', namespace='relationship_app')),
]
