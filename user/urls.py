from django.urls import path, include
from . import views
from rest_framework import urls


app_name = 'user'

urlpatterns = [
    path('join/', views.Join.as_view(), name='join'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('list/', views.UserList.as_view(), name='user-list'),
    path('profile/<int:pk>/', views.MyProfile.as_view(), name='view-profile'),
	# path('profile/write/', views.ProfileWrite.as_view(), name='wr-profile'),
	path('profile/update/', views.ProfileUpdate.as_view(), name='up-profile'),
	path('profile/delete/', views.ProfileDelete.as_view(), name='de-profile'),
    path("profile/change-password/", views.ChangePassword.as_view(), name="change-password"),
]