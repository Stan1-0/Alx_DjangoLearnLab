from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

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
