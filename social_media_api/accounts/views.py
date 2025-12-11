from django.shortcuts import render
from accounts.serializers import CustomUserSerializer, RegisterSerializer, LoginSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class CustomUserRegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
        
class CustomUserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

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
