from django.contrib.auth import views
from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from .views import register, LoginView, LogoutView


urlpatterns = [
    path('', list_books, name='list-all-books'),
    path('<int:library_pk>/books/', LibraryDetailView.as_view(), name="library_book_list"),
    path('<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path("register/", register.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    

]
