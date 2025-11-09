from django.shortcuts import render, redirect
from .models import Book
from .models import Library 
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView

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
    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

class LoginView(LoginView):
    template_name = "relationship_app/login.html"
    redirect_authenticated_user = True

class LogoutView(LogoutView):
    template_name = "relationship_app/logout.html"

