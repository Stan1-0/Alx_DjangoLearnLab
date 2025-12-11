from django.contrib.auth.forms import UserCreationForm, AdminUserCreationForm
from .models import CustomUser

class CustomUserCreationForm(AdminUserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'bio')
        
class CustomUserChangeForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'bio', 'profile_picture')
        
        