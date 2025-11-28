# api/views.py
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

# ---------------------------
# Book Views
# ---------------------------

class BookListCreateView(generics.ListCreateAPIView):
    """
    GET: list all books (supports filtering/search/ordering)
    POST: create a new book (authenticated users only)
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer

    # Use filter backends to enable filtering, search, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Fields for exact filtering (via ?field=value)
    filterset_fields = ['title', 'publication_year', 'author', 'author__name']

    # Search fields for text search (via ?search=term)
    search_fields = ['title', 'author__name']

    # Ordering fields (via ?ordering=field or ?ordering=-field)
    ordering_fields = ['title', 'publication_year', 'id']
    ordering = ['title']  # default ordering


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: retrieve a single book
    PUT/PATCH: update an existing book (authenticated)
    DELETE: delete a book (authenticated)
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    # Permission class inherited from REST_FRAMEWORK default IsAuthenticatedOrReadOnly


# ---------------------------
# Author Views
# ---------------------------

class AuthorListCreateView(generics.ListCreateAPIView):
    """
    GET: list authors
    POST: create author (authenticated)
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Author detail (GET), update (PUT/PATCH), delete (DELETE)
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
