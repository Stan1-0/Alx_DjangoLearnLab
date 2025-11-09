from django.shortcuts import render, redirect
from .models import Book
from .models import Library 
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile

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

def Admin(user):
    """
    Check if user is authenticated and has 'admin' role.
    Only users with the 'Admin' role can access admin views.
    """
    # Check if user is authenticated first
    if not user.is_authenticated:
        return False
    # Safely check if user has a profile and if the role is 'admin'
    try:
        return user.profile.role == 'admin'
    except UserProfile.DoesNotExist:
        # User doesn't have a profile
        return False
@user_passes_test(Admin)
def admin_dashboard(request):
    return render(request, 'relationship_app/admin_view.html')


def Librarian(user):
    return hasattr(user, 'profile') and user.profile.role == 'librarian'
@user_passes_test(Librarian)
def librarian_dashboard(request):
    return render(request, 'relationship_app/librarian_view.html')


def Member(user):
    return hasattr(user, 'profile') and user.profile.role == 'member'
@user_passes_test(Member)
def member_dashboard(request):
    return render(request, 'relationship_app/member_view.html')