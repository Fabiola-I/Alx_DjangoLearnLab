from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification

# -------------------------------
# Post CRUD
# -------------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# -------------------------------
# Comment CRUD
# -------------------------------
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# -------------------------------
# Like Post
# -------------------------------
@api_view(['POST'])
def like_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)  # 🔴 REQUIRED BY ALX

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )  # 🔴 REQUIRED BY ALX

    if created:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            target=post
        )  # 🔴 REQUIRED BY ALX

        return Response(
            {'detail': 'Post liked'},
            status=status.HTTP_201_CREATED
        )

    return Response(
        {'detail': 'Post already liked'},
        status=status.HTTP_200_OK
    )

# -------------------------------
# Unlike Post
# -------------------------------
@api_view(['POST'])
def unlike_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)

    Like.objects.filter(
        user=request.user,
        post=post
    ).delete()

    return Response(
        {'detail': 'Post unliked'},
        status=status.HTTP_200_OK
    )
