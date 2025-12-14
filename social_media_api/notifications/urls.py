from django.urls import path
from .views import RegisterView, LoginView, follow_user, unfollow_user, feed

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('follow/<int:user_id>/', follow_user, name='follow'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow'),
    path('feed/', feed, name='feed'),
]
