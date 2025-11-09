from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def is_member(user):
    return hasattr(user, 'profile') and user.profile.role == 'member'

@user_passes_test(is_member)
def member_dashboard(request):
    return render(request, 'relationship_app/member_view.html')