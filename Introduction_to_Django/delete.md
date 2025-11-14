### Delete the Book

```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
```

### Expected Output:
```python
[]  # Empty QuerySet → book is deleted
```
