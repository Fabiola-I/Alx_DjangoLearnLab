from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView, UserListView, FollowUserView, UnfollowUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('users/', UserListView.as_view(), name='user-list'),

    # 🔴 ALX requires user_id (NOT pk)
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
]
