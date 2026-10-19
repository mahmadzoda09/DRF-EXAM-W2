from django.db import models
from accounts.models import Account

class Chat(models.Model):
    user_1 = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='chats_user1')
    user_2 = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='chats_user2')
    cr_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Chat: {self.user_1} - {self.user_2}'

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE,related_name='messages')
    sender = models.ForeignKey(Account, on_delete=models.CASCADE,related_name= 'sent_messages')
    content = models.TextField()
    cr_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}: {self.content[:30]}'