from django.shortcuts import render
from .models import Book
from .models import Library 
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.views.generic import CreateView

# Create your views here.
def list_books(request):
    #Query all books and their associated authors
    books = Book.objects.all()
    
    #Create a list of tuples
    book_list = [(book.title, book.author) for book in books]
    
    return render(request, 'relationship_app/list_books.html',{'books': book_list})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html' 
    context_object_name = 'library'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library_id = self.kwargs['pk']
        library = Library.objects.get(id=library_id)
        library_books = library.books.all()
        books = [Book.objects.get(pk=book.id) for book in library_books]
        context.update({'books': books})
        return context
    
class register(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "relationship_app/register.html"

class LoginView(LoginView):
    template_name = "relationship_app/login.html"
    redirect_authenticated_user = True

class LogoutView(LogoutView):
    template_name = "relationship_app/logout.html"