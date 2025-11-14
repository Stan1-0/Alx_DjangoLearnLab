from django.contrib import admin
from .models import *

# Register your models here.
class Bookadmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_year']
    list_filter = ['author', 'publication_year']
    search_fields = ('author', 'title')

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'date_of_birth']
    list_filter = ['date_of_birth']
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["date_of_birth"]}),
        ("Permissions", {"fields": ["is_staff", "is_superuser"]}),
    ]
   
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "date_of_birth", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

admin.site.register(Book, Bookadmin)

admin.site.register(CustomUser, CustomUserAdmin)