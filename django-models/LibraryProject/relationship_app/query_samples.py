from relationship_app.models import Author, Book, Library, Librarian

# Clear existing data to avoid duplicates
Book.objects.all().delete()
Author.objects.all().delete()
Library.objects.all().delete()
Librarian.objects.all().delete()

# Create Authors
author1 = Author.objects.create(name="George Orwell")
author2 = Author.objects.create(name="J.K. Rowling")

# Create Books
book1 = Book.objects.create(title="1984", author=author1)
book2 = Book.objects.create(title="Animal Farm", author=author1)
book3 = Book.objects.create(title="Harry Potter 1", author=author2)

# Create Library
library1 = Library.objects.create(name="Central Library")
library1.books.set([book1, book2, book3])

# Create Librarian
librarian1 = Librarian.objects.create(name="Alice", library=library1)

# -------------------------
# Run queries
# -------------------------

# 1️⃣ Query all books by George Orwell
author = Author.objects.get(name="George Orwell")
books_by_author = author.books.all()
print(f"Books by {author.name}: {[book.title for book in books_by_author]}")

# 2️⃣ List all books in Central Library
library = Library.objects.get(name="Central Library")
books_in_library = library.books.all()
print(f"Books in {library.name}: {[book.title for book in books_in_library]}")

# 3️⃣ Retrieve the librarian for Central Library
librarian = library.librarian
print(f"Librarian of {library.name}: {librarian.name}")
