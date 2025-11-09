from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    
    def __str__(self):
        return self.title
    
class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name="books")
    
    def __str__(self):
        return self.name
    
class Librarian(models.Model):
    name = models.CharField(max_length=200)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name="Library")
    
    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    ROLES = [
        ('admin', 'Admin'),
        ('librarian', 'Librarian'),
        ('member', 'Member'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLES, default='user')
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    