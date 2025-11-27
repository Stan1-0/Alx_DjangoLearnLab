from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import *

# Create your views here.
class BookListView(generics.ListAPIView):
    #view for listing all books(GET)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    permission_classes =[permissions.AllowAny]
    
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
    
    