from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from .models import User, Profile
from .serializers import UserLoginSerializer, UserJoinSerializer, ProfileSerializer, UserSerializer
from .renderers import UserJSONRenderer
# Create your views here.

### Login 수정 중
# class Login(generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserLoginSerializer
    # def post(self, request):
    #     email = request.data.post('email')
    #     password = request.data.post('password')
    #     user = User.objects.filter(email=email).first()
    #     serializer = UserLoginSerializer(email = email, password = password)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
        
        # if email is None:
        #     return Response({'msg' : '이메일이 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # if not check_password(password, user.password):
        #     return Response({'msg' : '비밀번호가 틀렸습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class Join(APIView):
    # queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserJoinSerializer
    renderer_classes = (UserJSONRenderer,)
    def post(self, request):
        user = request.data
        
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)




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