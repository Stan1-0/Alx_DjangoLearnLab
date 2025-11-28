from django_filters import rest_framework
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import filters

# Create your views here.
work = filters.OrderingFilter

class AuthorCreateView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
class AuthorDetailView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
class BookListView(generics.ListAPIView):
    #view for listing all books(GET)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'publication_year']
    
    permission_classes =[permissions.AllowAny]
    
    def get_queryset(self):
        #checking for search term in request
        queryset = super().get_queryset(self)
        search_term = self.request.GET.get('search')
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(author__icontains=search_term)   
            )
        return queryset
        
    
class BookDetailView(generics.RetrieveAPIView):
    #view for listing a single book by id(GET)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    
class BookCreateView(generics.CreateAPIView):
    #view for creating a new book(POST)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        today = date.today().year
        if serializer.validated_data['publication_year'] > today:
            raise serializers.ValidationError("Publication year cannot be in the future")
        
        serializer.save(author=self.request.user)
    
class BookUpdateView(generics.UpdateAPIView):
    #view for updating an existing book(PUT)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    permission_classes = [IsAuthenticated]
    
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
    
    permission_classes = [IsAuthenticated]
    
    