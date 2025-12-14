from django.shortcuts import render
from accounts.serializers import CustomUserSerializer, RegisterSerializer, LoginSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import CustomUser
from rest_framework import status
from django.shortcuts import get_object_or_404
from notifications.utils import create_notification


# Create your views here.
class CustomUserRegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
        
class CustomUserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            "user": CustomUserSerializer(serializer.validated_data["user"]).data,
            "token": serializer.validated_data["token"]
        })

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, id=user_id)

        if user_to_follow == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.following.add(user_to_follow)
        
        create_notification(
            recipient=user_to_follow,
            actor=request.user,
            verb="started following you"
        )

        return Response({
            "message": f"You are now following {user_to_follow.username}.",
            "following_count": request.user.following.count()
        })

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)

        request.user.following.remove(user_to_unfollow)

        return Response({
            "message": f"You unfollowed {user_to_unfollow.username}.",
            "following_count": request.user.following.count()
        })


class GetFollowersListView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.followers.all()
    
#permissions.IsAuthenticated
#CustomUser.objects.all()