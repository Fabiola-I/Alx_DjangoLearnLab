# api/serializers.py
from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

# ----------------------------------------------------------------
# BookSerializer
# - Serializes all Book fields
# - Validates publication_year is not in the future
# ----------------------------------------------------------------
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """Ensure the publication year is not in the future."""
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# ----------------------------------------------------------------
# AuthorSerializer
# - Serializes Author.name and includes nested BookSerializer
# - Nested books are read-only; Book create/update uses Book endpoints
# ----------------------------------------------------------------
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # uses related_name='books'

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
