from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from .forms import ExampleForm
from .models import Book

# Create your views here.
@permission_required('bookshelf.can_view', raise_exception=True)
def ExampleView(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/form_example.html', {'books': books})