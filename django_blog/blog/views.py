from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import RegistrationForm, PostForm
from .models import Post

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {"form": form}

    return render(request, "blog/register.html", context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                # Check for 'next' parameter to redirect after login
                next_url = request.GET.get('next', None)
                if next_url:
                    return redirect(next_url)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    context = {"form": form}
    return render(request, "blog/login.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

def home(request):
    return render(request, "blog/home.html")

class PostListView(ListView):
    """
    List view for displaying all blog posts.
    Accessible to all users (authenticated and unauthenticated).
    """
    model = Post
    template_name = 'blog/posts.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10
    
    def get_queryset(self):
        """Return all published posts ordered by date."""
        return Post.objects.all().order_by('-published_date')


class PostDetailView(DetailView):
    """
    Detail view for displaying a single blog post.
    Accessible to all users (authenticated and unauthenticated).
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Create view for creating new blog posts.
    Requires authentication - only logged-in users can create posts.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('posts')
    login_url = '/blog/login/'
    
    def form_valid(self, form):
        """Set the author to the current user before saving."""
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update view for editing existing blog posts.
    Requires authentication AND only the post author can edit.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('posts')
    login_url = '/blog/login/'
    
    def form_valid(self, form):
        """Show success message after updating."""
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        """Check if the current user is the author of the post."""
        post = self.get_object()
        return self.request.user == post.author
    
    def handle_no_permission(self):
        """Handle unauthorized access attempts."""
        messages.error(self.request, 'You do not have permission to edit this post.')
        return redirect('post-detail', pk=self.get_object().pk)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete view for removing blog posts.
    Requires authentication AND only the post author can delete.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('posts')
    context_object_name = 'post'
    login_url = '/blog/login/'
    
    def test_func(self):
        """Check if the current user is the author of the post."""
        post = self.get_object()
        return self.request.user == post.author
    
    def handle_no_permission(self):
        """Handle unauthorized access attempts."""
        messages.error(self.request, 'You do not have permission to delete this post.')
        return redirect('post-detail', pk=self.get_object().pk)
    
    def delete(self, request, *args, **kwargs):
        """Show success message after deletion."""
        messages.success(self.request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to view your profile.')
        return redirect('login')
    
    # Get user's posts
    user_posts = Post.objects.filter(author=request.user).order_by('-published_date')
    context = {
        'user': request.user,
        'user_posts': user_posts,
    }
    return render(request, "blog/profile.html", context)