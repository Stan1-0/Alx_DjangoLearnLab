from django.shortcuts import render
from .models import Book, Library
from django.views.generic import DetailView

# Create your views here.
def list_all_books(request):
    #Query all books and their associated authors
    books = Book.objects.all()
    
    #Create a list of tuples
    book_list = [(book.title, book.author.name) for book in books]
    
    return render(request, 'relationship_app/list_books.html',{'books': book_list})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html' 
    context_object_name = 'library'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library_id = self.kwargs['pk']
        library_books = LibraryBook.objects.filter(library=library_id)
        books = [Book.objects.get(pk=book.book.id) for book in library_books]

        context.update({'books': books})
        return context