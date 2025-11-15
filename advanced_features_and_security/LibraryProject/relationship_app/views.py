from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import login, get_user_model
from django.views.generic import DetailView
from django.views.decorators.cache import cache_page 
from django.contrib.auth.forms import UserCreationForm

# Imports the forms, models, and Celery task
from .forms import BookForm 
from .models import Author, Book, Library, Librarian 
from .tasks import send_new_book_notification_email 

# Get the Custom User Model
User = get_user_model()


# ----------------------------
# Views with Permission Checks and Caching
# FIX: Added @login_required to ensure anonymous users redirect (302) instead of getting 403.
# ----------------------------

@cache_page(300) 
@login_required # <--- ADDED THIS LINE
@permission_required('relationship_app.can_view', raise_exception=True)
def list_books(request):
    """Requires 'can_view' permission to see the list of books, and caches the result."""
    books = Book.objects.all() 
    return render(request, "relationship_app/list_books.html", {"books": books})

@login_required # <--- ADDED THIS LINE
@permission_required('relationship_app.can_view', raise_exception=True)
def book_detail(request, pk):
    """Requires 'can_view' permission to see a specific book's details."""
    book = get_object_or_404(Book, pk=pk)
    # This view requires the template: relationship_app/book_detail.html
    return render(request, 'relationship_app/book_detail.html', {'book': book})

@login_required # <--- ADDED THIS LINE
@permission_required('relationship_app.can_create', raise_exception=True)
def add_book(request):
    """Requires 'can_create' permission to add a new book."""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            
            # --- CELERY INTEGRATION: Trigger the email task asynchronously ---
            recipient_email = request.user.email if request.user.email else "admin@library.com"
            send_new_book_notification_email.delay(
                book.title, 
                recipient_email
            )
            # -----------------------------------------------------------------
            
            return redirect('relationship_app:list_books')
    else:
        form = BookForm()
        
    return render(request, 'relationship_app/add_book.html', {'form': form})

@login_required # <--- ADDED THIS LINE
@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, pk):
    """Requires 'can_edit' permission to modify an existing book."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save() 
            return redirect('relationship_app:list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

@login_required # <--- ADDED THIS LINE
@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_book(request, pk):
    """Requires 'can_delete' permission to remove a book."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete() 
        return redirect('relationship_app:list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})


# ----------------------------
# Class-Based View: library detail
# ----------------------------

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# ----------------------------
# Role-Based Views (Based on role attribute in CustomUser)
# These views should also be protected by @login_required if they access sensitive data
# ----------------------------

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'role') and user.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'role') and user.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'role') and user.role == 'Member'

@login_required # <--- ADDED THIS LINE
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@login_required # <--- ADDED THIS LINE
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@login_required # <--- ADDED THIS LINE
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


# ----------------------------
# Registration View
# ----------------------------

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('relationship_app:list_books') 
    else:
        form = UserCreationForm()
        
    return render(request, 'relationship_app/register.html', {'form': form})