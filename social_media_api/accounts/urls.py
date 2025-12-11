from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.CustomUserRegisterView.as_view(), name='register'),
    path('login/', views.CustomUserLoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),  
]
