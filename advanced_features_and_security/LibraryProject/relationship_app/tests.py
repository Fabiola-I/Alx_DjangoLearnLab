from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from .models import Author, Book # Import all necessary models

User = get_user_model()

# Helper function to get the URL names
def get_url(view_name, pk=None):
    if pk is not None:
        return reverse(f'relationship_app:{view_name}', args=[pk])
    return reverse(f'relationship_app:{view_name}')

# The primary fix for the ModuleNotFoundError/2FA conflict during testing:
# Temporarily override AUTHENTICATION_BACKENDS to use only the standard ModelBackend.
@override_settings(AUTHENTICATION_BACKENDS=[
    'django.contrib.auth.backends.ModelBackend',
])
class BookPermissionTest(TestCase):
    """Tests permissions enforcement on Book CRUD views."""

    @classmethod
    def setUpTestData(cls):
        # 1. Create permissions required for the app
        cls.view_perm = Permission.objects.get(codename='can_view')
        cls.create_perm = Permission.objects.get(codename='can_create')
        cls.edit_perm = Permission.objects.get(codename='can_edit')
        cls.delete_perm = Permission.objects.get(codename='can_delete')

        # 2. Create groups
        cls.viewer_group = Group.objects.create(name='Viewer')
        cls.editor_group = Group.objects.create(name='Editor')

        # 3. Assign permissions to groups
        cls.viewer_group.permissions.add(cls.view_perm)
        cls.editor_group.permissions.add(cls.view_perm, cls.create_perm, cls.edit_perm)

        # 4. Create Users
        cls.viewer_user = User.objects.create_user(
            username='viewer_user', 
            email='viewer@test.com',
            password='testpassword123'
        )
        cls.viewer_user.groups.add(cls.viewer_group)
        cls.viewer_user.save()

        cls.editor_user = User.objects.create_user(
            username='editor_user', 
            email='editor@test.com',
            password='testpassword123'
        )
        cls.editor_user.groups.add(cls.editor_group)
        cls.editor_user.save()

        # 5. Create test data
        cls.test_author = Author.objects.create(name="Test Author")
        cls.test_book = Book.objects.create(
            title="Test Book Title", 
            author=cls.test_author, 
            publication_year=2023
        )

        # 6. Define URLs
        cls.list_url = get_url('list_books')
        cls.detail_url = get_url('book_detail', cls.test_book.pk)
        cls.add_url = get_url('add_book')
        cls.edit_url = get_url('edit_book', cls.test_book.pk)
        cls.delete_url = get_url('delete_book', cls.test_book.pk)

    def setUp(self):
        self.client = Client()
        
    def test_anonymous_access_denied(self):
        """Anonymous user should be denied access to all views (redirect to login)."""
        # Since the views require permissions, anonymous users are denied access.
        # With the 2FA setting LOGIN_URL = 'two_factor:login', they should be redirected (status 302).
        
        # Test GET requests
        urls_to_test = [self.list_url, self.detail_url, self.add_url, self.edit_url, self.delete_url]
        for url in urls_to_test:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302, f"Anonymous access to {url} should redirect (302), not {response.status_code}")
            # Ensure the redirect goes to the LOGIN_URL
            self.assertIn(reverse('two_factor:login'), response.url, f"Anonymous access to {url} should redirect to login page.")

    def test_viewer_access(self):
        """Viewer should access list/detail but be denied add/edit/delete (expect 403)."""
        self.client.login(username='viewer_user', password='testpassword123')
        
        # Accessible views (requires 'can_view')
        self.assertEqual(self.client.get(self.list_url).status_code, 200)
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)

        # Restricted views (requires 'can_create', 'can_edit', 'can_delete')
        self.assertEqual(self.client.get(self.add_url).status_code, 403)
        self.assertEqual(self.client.get(self.edit_url).status_code, 403)
        self.assertEqual(self.client.get(self.delete_url).status_code, 403)

    def test_editor_permissions(self):
        """Editor should access list/add/edit but be denied delete (expect 403)."""
        self.client.login(username='editor_user', password='testpassword123')
        
        # Accessible views (requires 'can_view', 'can_create', 'can_edit')
        self.assertEqual(self.client.get(self.list_url).status_code, 200)
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)
        self.assertEqual(self.client.get(self.add_url).status_code, 200)
        self.assertEqual(self.client.get(self.edit_url).status_code, 200)
        
        # Restricted view (requires 'can_delete')
        self.assertEqual(self.client.get(self.delete_url).status_code, 403)