# api/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Author, Book

User = get_user_model()

class BookAPITestCase(APITestCase):
    def setUp(self):
        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()

        # authors
        self.author1 = Author.objects.create(name='Author One')
        self.author2 = Author.objects.create(name='Author Two')

        # books
        self.book1 = Book.objects.create(title='Alpha', publication_year=2000, author=self.author1)
        self.book2 = Book.objects.create(title='Beta', publication_year=2010, author=self.author1)
        self.book3 = Book.objects.create(title='Gamma', publication_year=2020, author=self.author2)

        self.list_url = reverse('book-list-create')
        self.detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})

    def test_list_books_public(self):
        """Anyone (unauthenticated) can list books."""
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # supports paginated responses or direct lists
        self.assertTrue('results' in resp.data or isinstance(resp.data, list))

    def test_retrieve_book(self):
        resp = self.client.get(self.detail_url(self.book1.pk))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['title'], 'Alpha')

    def test_create_book_requires_auth(self):
        data = {'title': 'Delta', 'publication_year': 2015, 'author': self.author1.pk}
        resp = self.client.post(self.list_url, data, format='json')
        # should be unauthorized
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # authenticate and try again
        self.client.force_authenticate(user=self.user)
        resp2 = self.client.post(self.list_url, data, format='json')
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp2.data['title'], 'Delta')

    def test_update_book_requires_auth(self):
        update_data = {'title': 'Alpha Updated', 'publication_year': 2001, 'author': self.author1.pk}
        resp = self.client.put(self.detail_url(self.book1.pk), update_data, format='json')
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        self.client.force_authenticate(user=self.user)
        resp2 = self.client.put(self.detail_url(self.book1.pk), update_data, format='json')
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.assertEqual(resp2.data['title'], 'Alpha Updated')

    def test_delete_book_requires_auth(self):
        resp = self.client.delete(self.detail_url(self.book2.pk))
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        self.client.force_authenticate(user=self.user)
        resp2 = self.client.delete(self.detail_url(self.book2.pk))
        self.assertEqual(resp2.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())

    def test_publication_year_validation(self):
        self.client.force_authenticate(user=self.user)
        future_year = 3000
        data = {'title': 'FutureBook', 'publication_year': future_year, 'author': self.author1.pk}
        resp = self.client.post(self.list_url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', resp.data)

    def test_filter_by_author_name(self):
        resp = self.client.get(self.list_url, {'author__name': 'Author One'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.data.get('results', resp.data)
        self.assertGreaterEqual(len(results), 1)
        for item in results:
            self.assertEqual(item['author'], self.author1.pk)

    def test_search_title(self):
        resp = self.client.get(self.list_url, {'search': 'Alpha'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.data.get('results', resp.data)
        self.assertTrue(any('Alpha' in item['title'] for item in results))

    def test_ordering_by_publication_year(self):
        resp = self.client.get(self.list_url, {'ordering': '-publication_year'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.data.get('results', resp.data)
        years = [item['publication_year'] for item in results]
        self.assertEqual(years, sorted(years, reverse=True))
