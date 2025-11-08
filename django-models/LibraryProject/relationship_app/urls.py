from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from .views import Register

urlpatterns = [
    path('', list_books, name='list-all-books'),
    path('<int:library_pk>/books/', LibraryDetailView.as_view(), name="library_book_list"),
    path('<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

]
