# django-models/LibraryProject/relationship_app/query_samples.py
# This script is intended to be run using 'python manage.py shell'

from relationship_app.models import Author, Book, Library, Librarian

def setup_initial_data():
    """Deletes existing data and creates new test data."""
    print("--- Setting up initial data ---")
    
    # Clean up old data for repeatable testing
    Author.objects.all().delete()
    
    # Authors & Books (ForeignKey Test)
    author_a, _ = Author.objects.get_or_create(name='Jane Austen')
    author_b, _ = Author.objects.get_or_create(name='Mark Twain')

    book_pnp, _ = Book.objects.get_or_create(title='Pride and Prejudice', author=author_a)
    book_huck, _ = Book.objects.get_or_create(title='Huckleberry Finn', author=author_b)
    book_sense, _ = Book.objects.get_or_create(title='Sense and Sensibility', author=author_a)
    
    # Library & Librarian (ManyToMany & OneToOne Tests)
    library_central, _ = Library.objects.get_or_create(name='Main City Library')
    # Link books to the library (ManyToManyField)
    library_central.books.set([book_pnp, book_huck]) 
    Librarian.objects.get_or_create(name='Sarah Connor', library=library_central)
    
    print("Data setup complete.")

def run_queries():
    """Executes the three required sample queries."""
    print("\n--- Running Sample Queries ---")

    # 1. Query all books by a specific author (Checks: "Query all books by a specific author.")
    print("\n**1. Books by Jane Austen (ForeignKey reverse lookup):**")
    try:
        author = Author.objects.get(name='Jane Austen')
        # Use the default reverse manager: book_set
        austin_books = author.book_set.all()
        for book in austin_books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print("Author not found.")

    # 2. List all books in a library (Checks: "List all books in a library.")
    print("\n**2. Books in Main City Library (ManyToManyField lookup):")
    try:
        library = Library.objects.get(name='Main City Library')
        # Direct access to the ManyToMany field 'books'
        library_books = library.books.all()
        for book in library_books:
            print(f"- {book.title}")
    except Library.DoesNotExist:
        print("Library not found.")
        
    # 3. Retrieve the librarian for a library (Checks: "Retrieve the librarian for a library.")
    print("\n**3. Librarian for Main City Library (OneToOne reverse lookup):**")
    try:
        library = Library.objects.get(name='Main City Library')
        # Reverse lookup uses the model name in lowercase: 'librarian'
        librarian = library.librarian
        print(f"Librarian: {librarian.name}")
    except Library.DoesNotExist:
        print("Library not found.")
    except Librarian.DoesNotExist:
        print("Librarian not found for this library.")

if __name__ == '__main__':
    setup_initial_data()
    run_queries()