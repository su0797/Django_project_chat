from rest_framework import serializers
from .models import User, Profile
from django.contrib.auth import authenticate
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","name", "email", "password", "is_staff", "is_superuser", "date_joined", "last_login"]



# class UserLoginSerializer(serializers.ModelSerializer):
#     def post(self, validated_data):
#         user = User.objects.get(
#             email = validated_data['email'],
#             password = validated_data['password']
#         )
#         return User
#     class Meta:
#         model = User
#         fields = ['email', 'password']


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # name = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    last_login = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )      
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        return user





# class UserJoinSerializer(serializers.ModelSerializer):
#     token = serializers.CharField(max_length=255, read_only=True)

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             name = validated_data['name'],
#             email = validated_data['email'],
#             password = validated_data['password']
#         )
#         return user
#     class Meta:
#         model = User
#         fields = ['name', 'email', 'password', 'token']

class UserJoinSerializer(serializers.ModelSerializer):
    
    token = serializers.CharField(max_length=255, read_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 
            'name',
            'password',
            'token'
            ]
    def create(self, validated_data):
        return User.objects.create(**validated_data)



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'