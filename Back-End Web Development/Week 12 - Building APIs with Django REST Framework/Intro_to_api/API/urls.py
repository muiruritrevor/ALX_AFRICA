from django.urls import path
from .views import BookListCreateAPIView, AuthorListCreateAPIView

urlpatterns = [
    path('api/books', BookListCreateAPIView.as_view(), name='book-list-create'),   # This maps the view to a URL
    path('api/author', AuthorListCreateAPIView.as_view(), name='Author'),
]
      