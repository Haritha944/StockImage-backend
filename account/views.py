from rest_framework import generics
from .serializers import RegisterSerializer
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
        return Response({"user": {"email": user.email, "phone_number": user.phone_number}}, status=status.HTTP_201_CREATED)