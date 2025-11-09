from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_books, name='list-all-books'),
    path('<int:library_pk>/books/', views.LibraryDetailView.as_view(), name="library_book_list"),
    path('<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path("register/", views.register, name="register"),
    path("login/", views.LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", views.LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("admin/", views.admin_dashboard, name="admin_view"),
    path("librarian/", views.librarian_dashboard, name="librarian_view"),
    path("member/", views.member_dashboard, name="member_view"),
    # Book CRUD views with permission checks
    path("book/add/", views.book_create, name="book_create"),
    path("book/<int:pk>/edit/", views.book_update, name="book_update"),
    path("book/<int:pk>/delete/", views.book_delete, name="book_delete"),
]
