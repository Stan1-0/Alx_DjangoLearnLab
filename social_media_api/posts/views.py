from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework.generics import ListAPIView
from notifications.utils import create_notification
from rest_framework .decorators import action

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at', 'updated_at']
    filterset_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.author != self.request.user:
            raise PermissionDenied()
        return obj
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like a post"""
        post = self.get_object()
        
        like, created = Like.objects.get_or_create(
            post=post,
            user=request.user
        )
        
        if not created:
            return Response(
                {"message": "You already liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create notification for post author
        create_notification(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post
        )
        
        return Response(
            {"message": "Post liked successfully."},
            status=status.HTTP_201_CREATED
        )

        
    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """Unlike a post"""
        post = self.get_object()
        
        try:
            like = Like.objects.get(post=post, user=request.user)
            like.delete()
            return Response(
                {"message": "Post unliked successfully."},
                status=status.HTTP_200_OK
            )
        except Like.DoesNotExist:
            return Response(
                {"message": "You haven't liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )
        

        if user in post.likes.all():
            post.likes.remove(user)
            post.save()
            return Response({'status': 'post unliked'})
        else:
            return Response({'status': 'post was not liked'}, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        queryset = Comment.objects.all()
        
        return queryset.filter(post_id=post_pk)

    def perform_create(self, serializer):
        post_pk = self.kwargs.get('post_pk')
        if post_pk is None:
            raise ValueError("Missing post_pk in URL")
        serializer.save(author=self.request.user, post_id=post_pk)

    def get_object(self):
        post_pk = self.kwargs.get('post_pk')
        comment_pk = self.kwargs.get('pk')

        obj = get_object_or_404(
            Comment,
            pk=comment_pk,
            post_id=post_pk
        )

        if obj.author != self.request.user:
            raise PermissionDenied("You do not own this comment")

        return obj
    
class UserFeedView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

#permissions.IsAuthenticated