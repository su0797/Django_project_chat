from django.urls import path
from .views import List, Write, Edit, Delete,  View

app_name = 'blog'

urlpatterns = [
    # 게시글
    path("", List.as_view(), name='list'),
    path("write/", Write.as_view(), name='write'),
    path('edit/<int:pk>/', Edit.as_view(), name='edit'),
    path('delete/<int:pk>/', Delete.as_view(), name='delete'),
    path('view/<int:pk>/', View.as_view(), name='view'),
]