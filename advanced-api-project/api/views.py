# api/views.py
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

# ----------------------
# Book views
# ----------------------
class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    Supports:
      - Filtering via ?title=... or ?publication_year=... or ?author=AUTHOR_ID
      - Search via ?search=some_text (searches title and author name)
      - Ordering via ?ordering=title or ?ordering=-publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # anyone can view list

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'publication_year', 'author']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering


class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<pk>/ -> get book detail
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # anyone can view details


class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/create/ -> create book
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT /api/books/<pk>/update/ -> update book
    Requires admin permission.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]  # only admin can update


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/<pk>/delete/ -> delete book
    Requires admin permission.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]  # only admin can delete


# ----------------------
# Author views
# ----------------------
class AuthorListView(generics.ListAPIView):
    """
    GET /api/authors/ -> list authors (with nested books)
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class AuthorDetailView(generics.RetrieveAPIView):
    """
    GET /api/authors/<pk>/ -> author detail with nested books
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
