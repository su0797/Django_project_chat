from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .models import Post
# Create your views here.

User = get_user_model


class List(APIView):
    def get(self, request):
        posts = Post.objects.order_by('created_at')

    