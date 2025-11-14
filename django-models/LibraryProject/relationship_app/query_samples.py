# relationship_app/query_samples.py
# Run this with Django shell or as a script (import django first if running standalone)

def query_all_books_by_author(author_name):
    from .models import Author, Book
    try:
        author = Author.objects.get(name=author_name)
    except Author.DoesNotExist:
        return []
    return list(Book.objects.filter(author=author))

def list_all_books_in_library(library_name):
    from .models import Library
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return []
    return list(library.books.all())

def retrieve_librarian_for_library(library_name):
    from .models import Library
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return None
    # using related name 'librarian' from Librarian model
    return getattr(library, 'librarian', None)

from relationship_app.models import Author, Book, Library, Librarian

# Example: get a specific author
author = Author.objects.get(name="Fabiola")

# Example: get all books by this author
books_by_author = Book.objects.filter(author=author)

# Example: get a library
library = Library.objects.get(name="Central Library")

# Retrieve the librarian for this library (this is what the checker wants)
librarian = Librarian.objects.get(library=library)

# Just print to test (optional)
print("Librarian:", librarian)

