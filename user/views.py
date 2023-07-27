from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from .models import User, Profile
from .serializers import UserLoginSerializer, UserJoinSerializer, ProfileSerializer, UserSerializer
# Create your views here.


class Login(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    # def post(self, request):
    #     email = request.data.get('email')
    #     password = request.data.get('password')
    #     user = User.objects.filter(email=email).first()
    #     serializer = UserLoginSerializer(user)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
        
        # if email is None:
        #     return Response({'msg' : '이메일이 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # if not check_password(password, user.password):
        #     return Response({'msg' : '비밀번호가 틀렸습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class Login(generics.)

#     if 

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Join(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserJoinSerializer


### Profile
class ProfileWrite(APIView):
    def post(self, request):
        user = request.data.get('user') # request.user
        image = request.data.get('image')
        age = request.data.get('age')

        profile = Profile.objects.create(user=user, image=image, age=age)
        serializer = ProfileSerializer(profile)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class ProfileUpdate(APIView):
    def get(self, request):
        profile = Profile.objects.get(user = request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
    def post(self, request):
        profile = Profile.objects.get(user = request.user)
        serializer = ProfileSerializer(profile, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ProfileDelete(APIView):
    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        profile.delete()
        return Response({'msg' : 'Profile deleted'}, status=status.HTTP_200_OK)