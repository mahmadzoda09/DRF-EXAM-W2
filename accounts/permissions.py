from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSelfOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user_id == request.user.id


class IsAvatarOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.profile.user_id == request.user.id
