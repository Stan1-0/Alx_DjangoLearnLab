from rest_framework import generics, viewsets
from .serializers import BookSerializer
from .models import Book
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


# Create your views here.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # TokenAuthentication: Requires token in Authorization header to identify the user
    authentication_classes = [TokenAuthentication]
    # IsAuthenticated: Only logged-in users (with valid token) can access this viewset
    permission_classes = [IsAuthenticated]

