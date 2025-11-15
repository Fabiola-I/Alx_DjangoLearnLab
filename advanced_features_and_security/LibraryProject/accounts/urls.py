from django.urls import path
from . import views

urlpatterns = [
    # Example path, adjust as needed
    path('', views.index, name='index'),
]
