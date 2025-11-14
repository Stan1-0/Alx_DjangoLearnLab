from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from .models import Book

# Create your views here.
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})