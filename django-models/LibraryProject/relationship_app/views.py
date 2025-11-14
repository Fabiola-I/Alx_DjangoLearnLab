# django-models/LibraryProject/relationship_app/views.py (FINAL COMPLETE)

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required # NEW IMPORT for Task 4

from .models import Book, Library, UserProfile # All models needed

# --- Task 1 & 2 Views (Existing) ---
def book_list(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    context_object_name = 'library' 
    template_name = 'relationship_app/library_detail.html'
    def get_queryset(self):
        return Library.objects.prefetch_related('books__author').all()

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# --- Task 3 Views (Existing) ---
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

# --- Task 4: Custom Permissions Enforcement ---

# Placeholder View for Adding (Checks for permission_required decorator and can_add_book)
@permission_required('relationship_app.can_add_book', login_url='login')
def book_add_view(request):
    # This would normally handle form submission to create a Book
    return render(request, 'relationship_app/permission_success.html', {'action': 'add'})

# Placeholder View for Editing (Checks for can_change_book)
@permission_required('relationship_app.can_change_book', login_url='login')
def book_edit_view(request, pk):
    # This would normally handle form submission to edit a Book
    # book = get_object_or_404(Book, pk=pk)
    return render(request, 'relationship_app/permission_success.html', {'action': 'edit'})

# Placeholder View for Deleting (Checks for can_delete_book)
@permission_required('relationship_app.can_delete_book', login_url='login')
def book_delete_view(request, pk):
    # This would normally handle deletion
    # book = get_object_or_404(Book, pk=pk).delete()
    return render(request, 'relationship_app/permission_success.html', {'action': 'delete'})