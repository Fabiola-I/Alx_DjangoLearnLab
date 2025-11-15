from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book
from .forms import BookForm
from django.http import HttpResponseForbidden
# LibraryProject/bookshelf/views.py
from django.shortcuts import render, redirect
from .forms import ExampleForm   # ✅ Add this line


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    qs = Book.objects.select_related('owner').all()
    return render(request, 'bookshelf/book_list.html', {'books': qs})


@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            return redirect('bookshelf:book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # Optionally enforce owner-based edit
    if not (request.user == book.owner or request.user.has_perm('bookshelf.can_edit')):
        return HttpResponseForbidden("You do not have permission to edit this book.")
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('bookshelf:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/form_example.html', {'form': form})
