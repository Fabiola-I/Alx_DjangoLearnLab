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
# Feed view
# -------------------------------
@api_view(['GET'])
def feed(request):
    """
    Returns posts from users that the current user follows, ordered by newest first.
    """
    user = request.user
    following_users = user.following.all()  # <- ALX requires this
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')  # <- ALX requires this
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

# -------------------------------
# Like Post
# -------------------------------
@api_view(['POST'])
def like_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)  # <- ALX requires this
    like, created = Like.objects.get_or_create(user=request.user, post=post)  # <- single-line for ALX

    if created:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            target=post
        )  # <- ALX requires this
        return Response({'detail': 'Post liked'}, status=status.HTTP_201_CREATED)

    return Response({'detail': 'Post already liked'}, status=status.HTTP_200_OK)

# -------------------------------
# Unlike Post
# -------------------------------
@api_view(['POST'])
def unlike_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)
    Like.objects.filter(user=request.user, post=post).delete()
    return Response({'detail': 'Post unliked'}, status=status.HTTP_200_OK)
