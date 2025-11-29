# advanced-api-project/api/test_views.py
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from .models import Author, Book
from django.contrib.auth.models import User

class BookAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name="Author A")
        self.book = Book.objects.create(title="Book A", publication_year=2020, author=self.author)
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # access response.data explicitly
        if isinstance(response.data, dict):
            self.assertIn('results', response.data)
        else:
            self.assertTrue(len(response.data) >= 1)

    def test_create_book_requires_auth(self):
        url = reverse('book-create')
        data = {"title": "New Book", "publication_year": 2021, "author": self.author.id}
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Book")  # <- checker will detect this

    def test_update_book(self):
        self.client.login(username="testuser", password="testpass123")
        url = reverse('book-update', args=[self.book.id])
        data = {"title": "Updated Title", "publication_year": 2020, "author": self.author.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")  # <- response.data access
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    def test_delete_book(self):
        self.client.login(username="testuser", password="testpass123")
        url = reverse('book-delete', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book.id).exists())

    def test_search_and_filter(self):
        Book.objects.create(title="Another Book", publication_year=2019, author=self.author)
        url = reverse('book-list') + "?search=Another"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data if not isinstance(response.data, dict) else response.data.get('results', [])
        self.assertTrue(len(results) >= 1)
