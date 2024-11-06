from rest_framework import generics
from .serializers import RegisterSerializer,LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

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