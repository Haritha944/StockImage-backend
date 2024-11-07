from rest_framework import generics
import environ
from .serializers import RegisterSerializer,LoginSerializer,PasswordResetConfirmSerializer,PasswordResetSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.core.mail import send_mail
from rest_framework import status
from .models import CustomUser
from dotenv import load_dotenv  
import os

load_dotenv()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully!"
            }, status=status.HTTP_201_CREATED)
        return Response({
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful!",
                "user": {
                    "email": user.email,
                    "phone_number": user.phone_number,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        user = CustomUser.objects.get(email=email)

       
        token = default_token_generator.make_token(user)
        frontend_url = os.getenv("FRONTEND_URL")
        uid = user.pk
        reset_link = f"{frontend_url}{reverse('password-reset-confirm')}?uid={uid}&token={token}"


        send_mail(
            subject="Password Reset Request",
            message=f"Click the link below to reset your password:\n{reset_link}",
            from_email=os.getenv("DEFAULT_FROM_EMAIL"),
            recipient_list=[email],
        )

        return Response({"detail": "Password reset link sent."}, status=status.HTTP_200_OK)
    
class PasswordResetConfirmView(APIView):
    def post(self,request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        new_password=serializer.validated_data['new_password']
        confirm_password=serializer.validated_data['confirm_password']
        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        if new_password != confirm_password:
            return Response({"detail": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(pk=uid)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Invalid user ID."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
