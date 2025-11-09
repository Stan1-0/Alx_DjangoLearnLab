from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Library, UserProfile
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from .forms import BookForm

# Create your views here.
def list_books(request):
    #Query all books and their associated authors
    books = Book.objects.all()
    
    return render(request, 'relationship_app/list_books.html', {'books': books})

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


# Book CRUD views with permission checks
@permission_required('relationship_app.can_add_book')
def book_create(request):
    """
    View to create a new book.
    Requires 'can_add_book' permission.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" has been created successfully.')
            return redirect('list-all-books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form, 'title': 'Add Book'})


@permission_required('relationship_app.can_change_book')
def book_update(request, pk):
    """
    View to update an existing book.
    Requires 'can_change_book' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" has been updated successfully.')
            return redirect('list-all-books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form, 'title': 'Edit Book', 'book': book})


@permission_required('relationship_app.can_delete_book')
def book_delete(request, pk):
    """
    View to delete a book.
    Requires 'can_delete_book' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" has been deleted successfully.')
        return redirect('list-all-books')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})