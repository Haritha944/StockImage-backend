from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'phone_number','is_active')
        read_only_fields = ('id', 'is_active')
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_phone_number(self, value):
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

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
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user=authenticate(email=email,password=password)
        if user is None:
            raise serializers.ValidationError("Invalid login credientials")
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")
        data['user'] = user
        return data
    
class PasswordResetSerializer(serializers.Serializer):
    email=serializers.EmailField()

    def validate_email(self,value):
        try:
            user=CustomUser.objects.filter(email=value).first()
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Email address is not registered here")
        return value
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    token = serializers.CharField()
    uid = serializers.CharField()