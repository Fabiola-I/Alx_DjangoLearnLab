# api/views.py
from rest_framework import generics, permissions
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

# Book views
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
    permission_classes = [permissions.AllowAny]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'publication_year', 'author']    # exact-match filters
    search_fields = ['title', 'author__name']                     # text search fields
    ordering_fields = ['title', 'publication_year']              # allowed ordering fields
    ordering = ['title']  # default ordering
class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<pk>/ -> get book detail
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


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
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/<pk>/delete/ -> delete book
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# Author views
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
