from django.urls import path
from .views import list_books
from .views import LibraryDetailView

urlpatterns = [
    path('<int:library_pk>/books/', list_books,name="list_all_books"),
    path('<int:pk>/', LibraryDetailView.as_view(), name='library_detail')
]
