from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Profile
# Create your views here.


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