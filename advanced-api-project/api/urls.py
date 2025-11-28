from django.urls import path
from .views import *

urlpatterns = [
    path('author/', AuthorListView.as_view(), name='author-list'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('author/<int:pk>/', AuthorDetailView.as_view(),name='author-detail'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('author/create/', AuthorCreateView.as_view(), name='author-list'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/update/<int:pk>', BookUpdateView.as_view(), name='book-update'),
    path('books/delete/<int:pk>', BookDeleteView.as_view(), name='book-delete')
]
