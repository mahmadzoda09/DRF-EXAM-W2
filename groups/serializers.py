from rest_framework import serializers
from .models import Group, GroupMember, GroupMessage


class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Group
        fields = ["id", "owner", "title", "avatar"]
        read_only_fields = ["id", "owner"]


class GroupMemberSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    group = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GroupMember
        fields = ["id", "user", "group", "role", "joining_date"]
        read_only_fields = ["id", "user", "group", "joining_date"]


class GroupMessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    group = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GroupMessage
        fields = ["id", "user", "group", "content", "cr_at"]
        read_only_fields = ["id", "user", "group", "cr_at"]