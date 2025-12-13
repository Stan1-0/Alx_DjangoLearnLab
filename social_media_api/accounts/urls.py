from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.CustomUserRegisterView.as_view(), name='register'),
    path('login/', views.CustomUserLoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),  
    path('follow/<int:user_id>/', views.FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', views.UnfollowUserView.as_view(), name='unfollow-user'),
    path('followers/', views.GetFollowersListView.as_view(), name='followers-list'),
]
