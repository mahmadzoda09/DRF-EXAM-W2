from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("user", "User"),
    )
    phone_number = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.phone_number


class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    username = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.username


class Avatar(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="avatar")
    image = models.ImageField(upload_to="avatars/")
    created_at = models.DateTimeField(auto_now_add=True)
