from django.contrib import admin
from .models import Book

# Custom admin configuration
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # columns to display
    search_fields = ('title', 'author')                    # search by title/author
    list_filter = ('publication_year',)                   # filter by year

# Register the model with the custom admin
admin.site.register(Book, BookAdmin)
