from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from django.contrib.auth import logout as django_logout  # Django의 logout 함수와 충돌을 피하기 위해 이름 변경
from rest_framework.authtoken.models import Token
from .models import User, Profile
from .serializers import UserLoginSerializer, UserJoinSerializer, ProfileSerializer, UserSerializer
from .renderers import UserJSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
# Create your views here.



class Login(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        email = request.data.get('email')  # 'uid'를 'email'로 수정
        password = request.data.get('password')  # 'upw'를 'password'로 수정
        data = {'email': email, 'password': password}
        serializer = self.serializer_class(data=data)
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



class Logout(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user  # 현재 로그인한 사용자
        try:
            token = Token.objects.get(user=user)  # 해당 사용자의 토큰 가져오기
            token.delete()  # 토큰 삭제
        except Token.DoesNotExist:
            pass

        # Django의 logout 함수 사용
        django_logout(request)

        return Response({"detail": "로그아웃되었습니다."}, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not user.check_password(current_password):
            return Response(
                data={"message": "현재 비밀번호가 일치하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        response = {"message": "비밀번호 변경이 완료되었습니다."}
        return Response(data=response, status=status.HTTP_200_OK)


### Profile
class ProfileWrite(APIView):
    def post(self, request):
        user = request.data.get('user') # request.user
        image = request.data.get('image')
        age = request.data.get('age')

        profile = Profile.objects.create(user=user, image=image, age=age)
        serializer = ProfileSerializer(profile)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ProfileView(APIView):
    def get(self, request, pk):
        raw_user = User.objects.get(id=pk)
        raw_user.save()

        user_data = UserSerializer(raw_user).data
        data = {
            "user" : user_data
        }
        return Response(data, status=status.HTTP_200_OK)
    

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