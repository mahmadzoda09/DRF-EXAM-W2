from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Account, Profile, Avatar
from .serializers import *
from .permissions import IsSelfOrReadOnly, IsAvatarOwner


class PhoneTokenSerializer(TokenObtainPairSerializer):
    username_field = Account.USERNAME_FIELD


class PhoneTokenObtainPairView(TokenObtainPairView):
    serializer_class = PhoneTokenSerializer


class RegisterView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(AccountSerializer(request.user).data)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user.check_password(serializer.validated_data["old_password"]):
            return Response({"old_password": ["Incorrect password."]}, status=status.HTTP_400_BAD_REQUEST)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response({"detail": "Password changed."})


class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.select_related("user").all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["username", "first_name", "last_name"]


class MyProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(
            user=request.user,
            defaults={"username": f"user_{request.user.id}"}
        )
        return Response(ProfileSerializer(profile).data)

    def patch(self, request):
        profile, _ = Profile.objects.get_or_create(
            user=request.user,
            defaults={"username": f"user_{request.user.id}"}
        )
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfileDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.select_related("user").all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class AvatarCreateView(generics.CreateAPIView):
    serializer_class = AvatarSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        profile, _ = Profile.objects.get_or_create(
            user=self.request.user,
            defaults={"username": f"user_{self.request.user.id}"}
        )
        serializer.save(profile=profile)


class AvatarDetailView(generics.RetrieveDestroyAPIView):
    queryset = Avatar.objects.select_related("profile", "profile__user").all()
    serializer_class = AvatarSerializer
    permission_classes = [permissions.IsAuthenticated, IsAvatarOwner]
