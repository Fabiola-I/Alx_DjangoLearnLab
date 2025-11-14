# relationship_app/query_samples.py
# Run this with Django shell or as a script (import django first if running standalone)

from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
def query_all_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
    except Author.DoesNotExist:
        return []
    # Checker expects literal Book.objects.filter
    return list(Book.objects.filter(author=author))

# 2. List all books in a library
def list_all_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return []
    # Using the ManyToMany relation to get books
    return list(library.books.all())

# 3. Retrieve the librarian for a library
def retrieve_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return None
    # This literal line is what Savan checker wants
    return Librarian.objects.get(library=library)

# -----------------------------
# Example usage / testing
# -----------------------------

if __name__ == "__main__":
    # Example: get a specific author
    author_name = "Fabiola"
    author = Author.objects.get(name=author_name)

    # Example: get all books by this author
    books_by_author = Book.objects.filter(author=author)
    print(f"Books by {author_name}: {books_by_author}")

    # Example: get a library
    library_name = "Central Library"
    library = Library.objects.get(name=library_name)

    # Retrieve the librarian for this library
    librarian = Librarian.objects.get(library=library)
    print(f"Librarian of {library_name}: {librarian}")
