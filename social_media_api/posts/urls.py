from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('<int:post_pk>/comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('<int:post_pk>/comments/<int:pk>', views.CommentDetailView.as_view(), name='comment-detail'),
]
