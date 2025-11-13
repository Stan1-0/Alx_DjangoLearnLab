from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField(null=True)
    
    def __str__(self):
        return self.title
    
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    def __str__(self):
        return self.username
    
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("A username is required")
        if not email:
            raise ValueError("An email is required")

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        extra_fields = {'is_active': True, 'is_staff': True}
        user = self.create_user(username, email, password, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user


    