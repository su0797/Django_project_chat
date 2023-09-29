from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer
from user.serializers import UserSerializer
# Create your views here.

User = get_user_model


class List(APIView):
    
    def get(self, request):
        posts = Post.objects.filter(is_active=True).order_by('-created_at')
        
        data = []
        for post in posts:
            post_info = {
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at,
                "updated_at": post.updated_at,
            }
            
            add_new = {
                "post": post_info
            }
            
            data.append(add_new)
        
        response_data = {
            "posts": data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    

class Write(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        post_data = {
            'title': request.data['title'],
            'content': request.data['content'],
            'writer': user
        }
        post = Post.objects.create(**post_data)

        data = {
            "message": "글 생성 완료"
        }
        return Response(data, status=status.HTTP_201_CREATED)
    

class Edit(APIView):
    # permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        post = Post.objects.get(id=pk)

        post.title = request.data.get('title', post.title)
        post.content = request.data.get('content', post.content)
        post.save()

        data = {
            "message": "글 수정 완료"
        }

        return Response(data, status=status.HTTP_200_OK)
    

class Delete(APIView):
    # permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        
        try:
            post = Post.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404
        
        post.is_active = False
        post.save()
        
        data = {
            "message": "글 삭제 완료"
        }
        return Response(data, status=status.HTTP_200_OK)
    

class View(APIView):
    # 좋아요, 글 정보, 댓글과 대댓글 구분
    def get(self, request, pk):
        raw_post = Post.objects.get(id=pk)
        raw_post.save()
        
        writer_info = UserSerializer(raw_post.writer).data 

        post_data = PostSerializer(raw_post).data

        data = {
            "post": post_data,
            "writer": writer_info
        }

        return Response(data, status=status.HTTP_200_OK)
    

class CommentWrite(APIView):
    # permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        post = Post.objects.get(id=request.data['post_id'])
        comment = Comment.objects.create(writer=user,content=request.data['content'],post=post,parent_comment=None)
        
        datas = {
            "message": "댓글 생성 완료",
        }
        return Response(datas,status=status.HTTP_201_CREATED)
    

class CommentDelete(APIView):
    # permission_classes = [IsAuthenticated]
    
    def post(self, request):
        comment = Comment.objects.get(id=request.data['comment_id'])
        comment.is_active = False
        comment.save()
        
        datas = {
            "message": "댓글 삭제 완료",
        }
        return Response(datas,status=status.HTTP_200_OK)