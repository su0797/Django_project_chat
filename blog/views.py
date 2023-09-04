from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .models import Post
# Create your views here.

User = get_user_model


class List(APIView):
    
    def post(self, request):
        posts = Post.objects.filter(is_active=True).order_by('-created_at')
        
        data = []
        for post in posts:
        post_info = {

        }
    