from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # 게시글
    path("", views.List.as_view(), name='list'),
    path("write/", views.Write.as_view(), name='write'),
    path('edit/<int:pk>/', views.Edit.as_view(), name='edit'),
    path('delete/<int:pk>/', views.Delete.as_view(), name='delete'),
    path('view/<int:pk>/', views.View.as_view(), name='view'),
    path('comment/write/', views.CommentWrite.as_view(), name='cm-write'),
    path('comment/delete/', views.CommentDelete.as_view(), name='cm-delete'),
    # 대댓글 기능 추가하기
]