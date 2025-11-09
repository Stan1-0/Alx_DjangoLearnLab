from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile

def is_admin(user):
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

@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'relationship_app/admin_view.html')