from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Token endpoint: POST username/password here to get authentication token
    path('api-token-auth/', views.obtain_auth_token),
    path('books',BookList.as_view(), name='book-list'),
    path('',include(router.urls)),
]