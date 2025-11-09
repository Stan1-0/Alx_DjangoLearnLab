from django.urls import path
from . import views
from . import admin_view
from . import librarian_view
from . import member_view

urlpatterns = [
    path('', views.list_books, name='list-all-books'),
    path('<int:library_pk>/books/', views.LibraryDetailView.as_view(), name="library_book_list"),
    path('<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path("register/", views.register, name="register"),
    path("login/", views.LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", views.LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("admin/", admin_view.admin_dashboard, name="admin_view"),
    path("librarian/", librarian_view.librarian_dashboard, name="librarian_view"),
    path("member/", member_view.member_dashboard, name="member_view"),

]
