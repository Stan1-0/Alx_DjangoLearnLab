from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, CommentViewSet, UserFeedView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'posts/<int:post_pk>/comments/',
        CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='comment-list-create'
    ),
    path(
        'posts/<int:post_pk>/comments/<int:pk>/',
        CommentViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'put': 'update',
            'delete': 'destroy'
        }),
        name='comment-detail'
    ),
    path('feed/', UserFeedView.as_view(), name='user-feed'),
    path('posts/<int:pk>/like/', PostViewSet.as_view({'post': 'like'}), name='post-like'),
    path('posts/<int:pk>/unlike/', PostViewSet.as_view({'post': 'unlike'}), name='post-unlike'),
]
