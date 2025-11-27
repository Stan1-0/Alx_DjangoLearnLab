from django.shortcuts import render
from rest_framework import generics
from .serializers import *

# Create your views here.
class BookListView(generics.ListAPIView):
    #view for listing all books(GET)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
class BookDetailView(generics.RetrieveAPIView):
    #view for listing a single book by id(GET)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    
class BookCreateView(generics.CreateAPIView):
    #view for creating a new book(POST)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
class BookUpdateView(generics.UpdateAPIView):
    #view for updating an existing book(PUT)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
class BookDeleteView(generics.DestroyAPIView):
    #view for deleting a book(DELETE)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    