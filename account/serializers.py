from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'phone_number','is_active')
        read_only_fields = ('id', 'is_active')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8, help_text="Password must be at least 8 characters long.")

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'password')  # Only fields required for registration

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])  # Hash the password before saving
        user.save()
        return user