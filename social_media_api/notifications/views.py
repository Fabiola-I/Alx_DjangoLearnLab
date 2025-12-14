from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from posts.models import Post
from posts.serializers import PostSerializer

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    target_user = User.objects.get(id=user_id)
    request.user.followers.add(target_user)
    return Response({"detail": f"You are now following {target_user.username}"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    target_user = User.objects.get(id=user_id)
    request.user.followers.remove(target_user)
    return Response({"detail": f"You have unfollowed {target_user.username}"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed(request):
    following_users = request.user.followers.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
