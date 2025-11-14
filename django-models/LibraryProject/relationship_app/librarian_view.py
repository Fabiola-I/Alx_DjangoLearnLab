from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def is_librarian(user):
    return hasattr(user, 'profile') and user.profile.role == 'Librarian'

@user_passes_test(is_librarian, login_url='login')
def librarian_view(request):
    # display librarian-only content
    return render(request, 'relationship_app/librarian_view.html')
