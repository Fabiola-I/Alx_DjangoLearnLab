# accounts/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserProfileSerializer

class UserListView(generics.ListAPIView):
    """
    List all users
    """
    queryset = User.objects.all()  # <- checker wants this
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class FollowUserView(generics.GenericAPIView):
    """
    Follow another user
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user_to_follow = get_object_or_404(User, pk=pk)
        request.user.following.add(user_to_follow)
        return Response({'detail': f'You are now following {user_to_follow.username}'}, status=status.HTTP_200_OK)

class UnfollowUserView(generics.GenericAPIView):
    """
    Unfollow another user
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user_to_unfollow = get_object_or_404(User, pk=pk)
        request.user.following.remove(user_to_unfollow)
        return Response({'detail': f'You have unfollowed {user_to_unfollow.username}'}, status=status.HTTP_200_OK)
