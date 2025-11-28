from rest_framework import serializers
from .models import *
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
        
    def validate_publication_year(self, value):
        today = date.today().year
        if value > today:
            raise serializers.ValidationError("Publication year cannot be in the future")
        return value
            
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['name', 'books']