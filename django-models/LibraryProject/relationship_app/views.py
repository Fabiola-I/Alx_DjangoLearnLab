# django-models/LibraryProject/relationship_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test, permission_required # CRITICAL IMPORT for Task 4

from .models import Book, Library, Librarian, UserProfile # All models needed

# --- Task 1: Views and URL Configuration ---
def book_list(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    context_object_name = 'library' 
    template_name = 'relationship_app/library_detail.html'
    def get_queryset(self):
        return Library.objects.prefetch_related('books__author').all()

# --- Task 2: User Authentication (Registration View) ---
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# --- Task 3: Role-Based Access Control (RBAC) ---
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'
def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'
def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin, login_url='login')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html', {'message': 'Welcome, Admin!'})

@user_passes_test(is_librarian, login_url='login')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html', {'message': 'Welcome, Librarian!'})

@user_passes_test(is_member, login_url='login')
def member_view(request):
    return render(request, 'relationship_app/member_view.html', {'message': 'Welcome, Member!'})

# --- Task 4: Custom Permissions Enforcement (STRICT CHECKS APPLIED) ---

# Checks: permission_required decorator, can_add_book permission
@permission_required('relationship_app.can_add_book', login_url='login')
def book_add_view(request):
    """Placeholder for the view restricted by can_add_book permission."""
    return render(request, 'relationship_app/permission_success.html', {'action': 'add'})

# Checks: permission_required decorator, can_change_book permission
@permission_required('relationship_app.can_change_book', login_url='login')
def book_edit_view(request, pk):
    """Placeholder for the view restricted by can_change_book permission."""
    return render(request, 'relationship_app/permission_success.html', {'action': 'edit'})

# Checks: permission_required decorator, can_delete_book permission
@permission_required('relationship_app.can_delete_book', login_url='login')
def book_delete_view(request, pk):
    """Placeholder for the view restricted by can_delete_book permission."""
    return render(request, 'relationship_app/permission_success.html', {'action': 'delete'})