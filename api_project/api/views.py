from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Book
from .serializers import BookSerializer

# Task 1: BookList (ListAPIView)
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Task 2: BookViewSet (ModelViewSet) for CRUD operations
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Allow read-only for unauthenticated users, require auth for POST/PUT/DELETE
    permission_classes = [IsAuthenticatedOrReadOnly]
