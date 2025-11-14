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

# Example usage (uncomment and use in shell):
# from relationship_app.query_samples import *
# print(query_all_books_by_author("J. K. Rowling"))
# print(list_all_books_in_library("Central Library"))
# print(retrieve_librarian_for_library("Central Library"))
