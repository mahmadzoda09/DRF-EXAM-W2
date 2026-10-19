from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Account, Profile, Avatar


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    class Meta:
        model = Account
        fields = ["id", "phone_number", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        account = Account.objects.create_user(
            username=validated_data['phone_number'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
        )
        return account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "phone_number", "role"]
        read_only_fields = ["id", "phone_number", "role"]


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "user_id", "first_name", "last_name", "bio", "username"]
        read_only_fields = ["id", "user_id"]


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ["id", "profile", "image", "created_at"]
        read_only_fields = ["id", "profile", "created_at"]