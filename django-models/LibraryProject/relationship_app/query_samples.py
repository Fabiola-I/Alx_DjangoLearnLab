from relationship_app.models import Author, Book, Library, Librarian

# 1️⃣ Query all books by a specific author
author = Author.objects.get(name="George Orwell")
books_by_author = author.books.all()
print(f"Books by {author.name}: {list(books_by_author)}")

# 2️⃣ List all books in a library
library = Library.objects.get(name="Central Library")
books_in_library = library.books.all()
print(f"Books in {library.name}: {list(books_in_library)}")

# 3️⃣ Retrieve the librarian for a library
librarian = library.librarian
print(f"Librarian of {library.name}: {librarian.name}")
