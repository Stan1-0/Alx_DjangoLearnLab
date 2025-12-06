from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import RegistrationForm, PostForm, CommentForm
from .models import Post, Comment
from django.db.models import Q

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
    Detail view for displaying a single blog post with comments.
    Accessible to all users (authenticated and unauthenticated).
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        """Add comments and comment form to the context."""
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.all()
        context['comment_form'] = CommentForm()
        return context


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

class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Create view for adding comments to blog posts.
    Requires authentication - only logged-in users can create comments.
    """
    model = Comment
    form_class = CommentForm
    login_url = '/blog/login/'
    
    def form_valid(self, form):
        """Set the post and author before saving. Ensure author cannot be tampered with."""
        post = Post.objects.get(pk=self.kwargs['pk'])
        form.instance.post = post
        # Security: Always set author from request.user, never trust form data
        form.instance.author = self.request.user
        messages.success(self.request, 'Comment added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect back to the post detail page after commenting."""
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update view for editing existing comments.
    Requires authentication AND only the comment author can edit.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    login_url = '/blog/login/'
    
    def form_valid(self, form):
        """Show success message after updating and ensure author cannot be changed."""
        # Security check: Ensure the author hasn't been tampered with
        comment = self.get_object()
        if form.instance.author != comment.author:
            form.instance.author = comment.author
        messages.success(self.request, 'Comment updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        """Check if the current user is the author of the comment."""
        if not self.request.user.is_authenticated:
            return False
        comment = self.get_object()
        return self.request.user == comment.author
    
    def handle_no_permission(self):
        """Handle unauthorized access attempts."""
        # Store comment before redirect to avoid multiple get_object() calls
        try:
            comment = self.get_object()
            post_pk = comment.post.pk
        except:
            # If we can't get the comment, redirect to posts list
            messages.error(self.request, 'You do not have permission to edit this comment.')
            return redirect('posts')
        messages.error(self.request, 'You do not have permission to edit this comment.')
        return redirect('post-detail', pk=post_pk)
    
    def get_success_url(self):
        """Redirect back to the post detail page after editing."""
        comment = self.get_object()
        return reverse_lazy('post-detail', kwargs={'pk': comment.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete view for removing comments.
    Requires authentication AND only the comment author can delete.
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    context_object_name = 'comment'
    login_url = '/blog/login/'
    
    def test_func(self):
        """Check if the current user is the author of the comment."""
        if not self.request.user.is_authenticated:
            return False
        comment = self.get_object()
        return self.request.user == comment.author
    
    def handle_no_permission(self):
        """Handle unauthorized access attempts."""
        # Store comment before redirect to avoid multiple get_object() calls
        try:
            comment = self.get_object()
            post_pk = comment.post.pk
        except:
            # If we can't get the comment, redirect to posts list
            messages.error(self.request, 'You do not have permission to delete this comment.')
            return redirect('posts')
        messages.error(self.request, 'You do not have permission to delete this comment.')
        return redirect('post-detail', pk=post_pk)
    
    def delete(self, request, *args, **kwargs):
        """Show success message after deletion and verify permissions again."""
        comment = self.get_object()
        # Double-check permission before deletion (defense in depth)
        if request.user != comment.author:
            messages.error(request, 'You do not have permission to delete this comment.')
            return redirect('post-detail', pk=comment.post.pk)
        messages.success(request, 'Comment deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        """Redirect back to the post detail page after deletion."""
        comment = self.get_object()
        return reverse_lazy('post-detail', kwargs={'pk': comment.post.pk})


@login_required(login_url='/blog/login/')
def profile(request):
    """
    Profile view for displaying user information and their posts.
    Requires authentication - only logged-in users can view their profile.
    """
    # Get user's posts
    user_posts = Post.objects.filter(author=request.user).order_by('-published_date')
    context = {
        'user': request.user,
        'user_posts': user_posts,
    }
    return render(request, "blog/profile.html", context)

def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if not query:
            return redirect('posts')

        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__iexact=query)
        ).distinct()

        context = {
            'query': query,
            'posts': posts
        }
        return render(request, 'blog/search_results.html', context)
    return redirect('posts')