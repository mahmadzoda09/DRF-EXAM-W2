from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Chat,Message


class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id','user_1','user_2','cr_at']
        read_only_fields = ['id','user_1']

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['id','sender','chat','content','cr_at']
        read_only_fields = ['id', 'chat', 'sender', 'cr_at']