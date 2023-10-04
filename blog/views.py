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

### Post
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
    

### Comment
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
    

class ReCommentWrite(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        try:
            post = Post.objects.get(id=request.data['post_id'])
        except:
            datas = {
                "message" : "해당 게시물을 찾을 수 없습니다."
            }
            return Response(datas, status=status.HTTP_400_BAD_REQUEST)
        else:
            parent_comment = Comment.objects.get(id=request.data['comment_id'])
            comment = Comment.objects.create(writer=user, content=request.data['content'], post=post, parent_comment=parent_comment)
            datas = {
                "message" : "대댓글 작성을 완료했습니다."
            }
            return Response(datas, status=status.HTTP_201_CREATED)
        

### Search
class Search(APIView):
    def post(self, request):
        query = request.data.get('query') 
        
        if query is None:
            return Response({"error": "Missing 'query' parameter"}, status=400)

        profiles = Profile.objects.filter(Q(nickname__icontains=query) | Q(about__icontains=query),is_active=True)
        
        new_profiles = []
        
        for pf in profiles:
            pf_serializer = UserSerializer(pf.user).data
            new_profiles.append(pf_serializer)
            
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query),is_active=True).order_by('-created_at')
        post_serializers = PostSerializer(posts, many=True).data
        
        studies = Study.objects.filter(Q(title__icontains=query) | Q(description__icontains=query),is_active=True).order_by('-created_at')
        study_serializer = StudySerializer(studies, many=True).data
        
        new_postlist = []
        
        for p_s in post_serializers:
            
            writer = User.objects.get(id=p_s['writer'])
            writer_info = UserSerializer(writer).data
            
            post_imgs = Post.objects.get(id=p_s['id'])
            images = post_imgs.image.all()  # 이미지들 가져오기
            p_s["images"]= [{"image": image.image.url} for image in images]
            
            info = {
                'post': p_s,
                'writer': writer_info
            }
            new_postlist.append(info)
        
        new_studies = []
        
        for s_s in study_serializer:
            leader = User.objects.get(id=s_s['leader'])
            leader_info = UserSerializer(leader).data
            info = {
                'study': s_s,
                'leader': leader_info
            }
            new_studies.append(info)
        
        response_data = {
            "profiles": new_profiles,
            "posts": new_postlist,
            "studies": new_studies
        }
        
        return Response(response_data)
