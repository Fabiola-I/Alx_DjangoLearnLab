from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import UserProfileSerializer, RegisterSerializer

# -------------------------
# User List
# -------------------------
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

# -------------------------
# Registration
# -------------------------
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = CustomUser.objects.get(id=response.data['id'])
        token, _ = Token.objects.get_or_create(user=user)
        response.data['token'] = token.key
        return response

# -------------------------
# Follow User
# -------------------------
class FollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(
            CustomUser.objects.all(), id=user_id
        )
        if user_to_follow == request.user:
            return Response(
                {'detail': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        request.user.following.add(user_to_follow)
        return Response(
            {'detail': f'You are now following {user_to_follow.username}'},
            status=status.HTTP_200_OK
        )

# -------------------------
# Unfollow User
# -------------------------
class UnfollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(
            CustomUser.objects.all(), id=user_id
        )
        if user_to_unfollow == request.user:
            return Response(
                {'detail': 'You cannot unfollow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        request.user.following.remove(user_to_unfollow)
        return Response(
            {'detail': f'You have unfollowed {user_to_unfollow.username}'},
            status=status.HTTP_200_OK
        )
