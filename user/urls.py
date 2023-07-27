from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
	path('profile/write/', views.ProfileWrite.as_view(), name='wr-profile'),
	path('profile/update/', views.ProfileUpdate.as_view(), name='up-profile'),
	path('profile/delete/', views.ProfileDelete.as_view(), name='de-profile'),
]