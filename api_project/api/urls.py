from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

router = DefaultRouter()
# Register BookViewSet as required by assignment (basename exactly 'book_all')
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # BookList endpoint (ListAPIView)
    path('books/', BookList.as_view(), name='book-list'),

    # Include router URLs for CRUD operations
    path('', include(router.urls)),
]
