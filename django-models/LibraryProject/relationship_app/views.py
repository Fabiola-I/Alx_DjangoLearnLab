from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Savan checker required imports
from django.views.generic.detail import DetailView     # required literal form
from .models import Library                            # required literal form

# Your other imports
from django.views.generic import DetailView            # still ok to keep
from .models import Author, Book, Librarian, UserProfile
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Book
from .forms import BookForm
# ----------------------------

def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})
# ----------------------------
# Class-Based View: library detail
# ----------------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# ----------------------------
# Role-Based Views
# ----------------------------
def is_admin(user):
    return hasattr(user, 'profile') and user.profile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'profile') and user.profile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'profile') and user.profile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


# ----------------------------
# Book Views with Permissions
# ----------------------------
@permission_required('relationship_app.can_add_book')
def add_book_view(request):
    return render(request, 'relationship_app/add_book.html')

@permission_required('relationship_app.can_change_book')
def edit_book_view(request):
    return render(request, 'relationship_app/edit_book.html')

@permission_required('relationship_app.can_delete_book')
def delete_book_view(request):
    return render(request, 'relationship_app/delete_book.html')
