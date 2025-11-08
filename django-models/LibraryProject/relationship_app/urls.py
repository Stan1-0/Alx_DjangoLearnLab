from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from .views import Register, CustomLoginView, CustomLogoutView


urlpatterns = [
    path('', list_books, name='list-all-books'),
    path('<int:library_pk>/books/', LibraryDetailView.as_view(), name="library_book_list"),
    path('<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path("register/", Register.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    

]
