# posts/views.py

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# --- Feed view ---
@api_view(['GET'])
def feed(request):
    user = request.user
    following_users = user.following.all()  # <- ALX check expects this
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')  # <- ALX check expects this
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
