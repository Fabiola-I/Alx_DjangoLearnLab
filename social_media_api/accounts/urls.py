# accounts/urls.py
from django.urls import path
from .views import UserListView, FollowUserView, UnfollowUserView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('follow/<int:pk>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:pk>/', UnfollowUserView.as_view(), name='unfollow-user'),
]
