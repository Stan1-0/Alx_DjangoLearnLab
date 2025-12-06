from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Tag
from taggit.forms import TagWidget, TagField


class RegistrationForm(UserCreationForm):
    # add additional fields
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    # include Meta class
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        
    tags = forms.Field(
        widget=TagWidget(attrs={'placeholder': 'Enter tags separated by commas'}),
        required=False,
    )

    def clean_tags(self):
        data = self.cleaned_data['tags']
        if data:
            # Convert comma-separated string to list of tags
            tags_list = data.split(',')
            # Strip whitespace from each tag
            tags_list = [tag.strip() for tag in tags_list]
            # Filter out empty tags
            tags_list = [tag for tag in tags_list if tag]
            
            # Create new tags if they don't exist
            existing_tags = Tag.objects.all()
            new_tags = []
            for tag in tags_list:
                try:
                    # If tag exists, add it to the queryset
                    new_tag = Tag.objects.get(name__iexact=tag)
                    new_tags.append(new_tag)
                except Tag.DoesNotExist:
                    # If tag doesn't exist, create it
                    new_tag = Tag.objects.create(name=tag)
                    new_tags.append(new_tag)
            
            # Update the cleaned data with the processed tags
            self.cleaned_data['tags'] = new_tags
        
        return self.cleaned_data['tags']


class CommentForm(forms.ModelForm):
    """
    Form for creating and updating comments.
    Includes validation rules for content length and required fields.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...',
                'required': True,
            }),
        }
        labels = {
            'content': 'Comment',
        }
        help_texts = {
            'content': 'Your comment must be between 10 and 2000 characters.',
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize the form and add custom attributes."""
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Write your comment here...',
        })
    
    def clean_content(self):
        """
        Validate comment content:
        - Must be at least 10 characters long
        - Must not exceed 2000 characters
        - Must not be empty or only whitespace
        """
        content = self.cleaned_data.get('content')
        
        if not content:
            raise forms.ValidationError('Comment content is required.')
        
        # Strip whitespace and check length
        content_stripped = content.strip()
        
        if len(content_stripped) < 10:
            raise forms.ValidationError(
                'Comment must be at least 10 characters long.'
            )
        
        if len(content) > 2000:
            raise forms.ValidationError(
                'Comment cannot exceed 2000 characters.'
            )
        
        # Return stripped content
        return content_stripped