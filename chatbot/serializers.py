from rest_framework import serializers
from .models import Conversation
from django.contrib.auth import authenticate
from django.utils import timezone


class ChatSerializer(serializers.Serializer):
    class Meta:
        model = Conversation
        fields = ['prompt', 'response']
    def create(self, validated_data):
        return Conversation.objects.create(**validated_data)
    

