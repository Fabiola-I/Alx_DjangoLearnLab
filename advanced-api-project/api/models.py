# api/models.py
from django.db import models

# ------------------------------------------
# Author Model
# ------------------------------------------
# Represents an author. Only the name field for simplicity.
# One Author can have many Book instances (one-to-many).
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# ------------------------------------------
# Book Model
# ------------------------------------------
# Represents a single book, linked to an Author via ForeignKey.
# publication_year is an integer and validated in serializers.
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'  # allows author.books.all()
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
