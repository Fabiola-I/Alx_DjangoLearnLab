# api/models.py
from django.db import models

class Author(models.Model):
    """
    Author model: stores the author's name.
    Purpose: represents an Author who can have multiple Books.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model: stores book details.
    Fields:
        - title: book title string
        - publication_year: integer year the book was published
        - author: foreign key to Author (one-to-many)
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
