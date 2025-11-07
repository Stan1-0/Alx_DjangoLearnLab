from django.urls import path
from .views import list_books
from .views import LibraryDetailView

urlpatterns = [
    path('list_books/', list_books,name="list_all_books"),
    path('library_detail/', LibraryDetailView.as_view(), name='library_detail')
]
