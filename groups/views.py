from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Group, GroupMember, GroupMessage
from .serializers import GroupSerializer, GroupMemberSerializer, GroupMessageSerializer


class GroupListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        group = serializer.save(owner=self.request.user)
        GroupMember.objects.get_or_create(
            user=self.request.user,
            group=group,
            defaults={"role": "owner"},
        )


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        group = self.get_object()

        if group.owner != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to update this group."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        group = self.get_object()

        if group.owner != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to delete this group."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().destroy(request, *args, **kwargs)


class GroupMemberListView(generics.ListAPIView):
    serializer_class = GroupMemberSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroupMember.objects.filter(group_id=self.kwargs["group_id"])


class JoinGroupView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id):
        group = Group.objects.filter(pk=group_id).first()

        if not group:
            return Response(
                {"detail": "Group not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        member, created = GroupMember.objects.get_or_create(
            user=request.user,
            group=group,
            defaults={"role": "member"},
        )

        if not created:
            return Response(
                {"detail": "You are already a member of this group."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            GroupMemberSerializer(member).data,
            status=status.HTTP_201_CREATED,
        )


class LeaveGroupView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, group_id):
        membership = GroupMember.objects.filter(
            group_id=group_id,
            user=request.user,
        ).first()

        if not membership:
            return Response(
                {"detail": "You are not a member of this group."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if membership.role == "owner":
            return Response(
                {"detail": "The owner cannot leave their own group."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupMessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroupMessage.objects.filter(
            group_id=self.kwargs["group_id"],
            group__members__user=self.request.user,
        ).order_by("cr_at")

    def list(self, request, *args, **kwargs):
        group_exists = Group.objects.filter(
            pk=self.kwargs["group_id"]
        ).exists()

        if not group_exists:
            return Response(
                {"detail": "Group not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not GroupMember.objects.filter(
            group_id=self.kwargs["group_id"],
            user=request.user,
        ).exists():
            return Response(
                {"detail": "You must join the group to view its messages."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        group = Group.objects.filter(pk=self.kwargs["group_id"]).first()

        if not group:
            return Response(
                {"detail": "Group not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not GroupMember.objects.filter(
            group=group,
            user=request.user,
        ).exists():
            return Response(
                {"detail": "You must join the group to send messages."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, group=group)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )