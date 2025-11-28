from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# ---------------------------
# List all books
# ---------------------------
class BookListView(generics.ListAPIView):
    """
    GET /books/
    Retrieve all books.
    Access: Public (AllowAny)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# ---------------------------
# Retrieve a single book by ID
# ---------------------------
class BookDetailView(generics.RetrieveAPIView):
    """
    GET /books/<int:pk>/
    Retrieve details of a single book by its ID.
    Access: Public (AllowAny)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# ---------------------------
# Create a new book
# ---------------------------
class BookCreateView(generics.CreateAPIView):
    """
    POST /books/create/
    Create a new book entry.
    Access: Authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Customize behavior if needed (e.g., auto-assign fields)
    def perform_create(self, serializer):
        serializer.save()

# ---------------------------
# Update an existing book
# ---------------------------
class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /books/update/<int:pk>/
    Update a book's details.
    Access: Authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Customize behavior if needed (e.g., logging updates)
    def perform_update(self, serializer):
        serializer.save()

# ---------------------------
# Delete a book
# ---------------------------
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /books/delete/<int:pk>/
    Delete a book entry.
    Access: Authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
