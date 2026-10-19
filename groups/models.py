from django.db import models
from accounts.models import Account


class Group(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='owned_groups')
    title = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='avatar/',blank=True,null=True)

    def __str__(self):
        return self.title

class GroupMember(models.Model):

    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]
    user = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='group_memberships')
    group = models.ForeignKey(Group, on_delete=models.CASCADE,related_name='members')
    role = models.CharField(max_length=50,choices=ROLE_CHOICES,default='member')
    joining_date = models.DateTimeField(auto_now_add=True)


class GroupMessage(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='group_messages')
    group = models.ForeignKey(Group, on_delete=models.CASCADE,related_name='messages')
    content = models.TextField()
    cr_at = models.DateTimeField(auto_now_add=True) 