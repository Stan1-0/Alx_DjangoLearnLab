from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

# Create your views here.
class BookListView(generics.ListAPIView):
    #view for listing all books(GET)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author']
    
    permission_classes =[permissions.AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset(self)
        return queryset.filter(
            Q(title_icontains=self.request.GET.get('search')) |
            Q(author_icontains=self.request.GET.get('search'))   
        )
        
    
class BookDetailView(generics.RetrieveAPIView):
    #view for listing a single book by id(GET)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    permission_classes = [permissions.AllowAny]
    
    
class BookCreateView(generics.CreateAPIView):
    #view for creating a new book(POST)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        today = date.today().year
        if serializer.validated_data['publication_year'] > today:
            raise serializers.ValidationError("Publication year cannot be in the future")
        
        serializer.save(author=self.request.user)
    
class BookUpdateView(generics.UpdateAPIView):
    #view for updating an existing book(PUT)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_update(self, serializer):
        today = date.today().year
        if serializer.validated_data['publication_year'] > today:
            raise serializers.ValidationError("Publication year cannot be in the future. ")
        
        book = self.get_object()
        if book.author != self.request.user:
            raise permissions.PermissionDenied("Only the owner can update this book. ")
    
class BookDeleteView(generics.DestroyAPIView):
    #view for deleting a book(DELETE)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    permission_classes = [permissions.IsAuthenticated]
    
    