### Update the Book Title

```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book.title
```

### Expected Output:
```python
'Nineteen Eighty-Four'
```
