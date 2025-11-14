# CRUD Operations for Book Model

## 1. Create
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
```

## 2. Retrieve
```python
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year
```

## 3. Update
```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book.title
```

## 4. Delete
```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
```
