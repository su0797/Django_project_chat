from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User, Profile
from django.contrib.auth import authenticate
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","name", "email", "password", "is_staff", "is_superuser", "date_joined", "last_login"]



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
# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(max_length=128, write_only=True)

#     def validate(self, data):
#         email = data.get('email', None)
#         password = data.get('password', None)
#         if email is None:
#             raise serializers.ValidationError('이메일 주소를 입력해주세요.')
#         if password is None:
#             raise serializers.ValidationError('비밀번호를 입력해주세요.')

#         user = authenticate(email=email, password=password)

#         if user is None:
#             raise serializers.ValidationError('해당 이메일과 비밀번호를 가진 사용자를 찾을 수 없습니다.')
#         if not user.is_active:
#             raise serializers.ValidationError('이 사용자는 비활성화되었습니다.')

#         token, _ = Token.objects.get_or_create(user=user)  # 사용자의 토큰 가져오기

#         return {
#             'user': user,
#             'access_token': token.key,  # 토큰 값을 'access_token'으로 변경
#         }



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