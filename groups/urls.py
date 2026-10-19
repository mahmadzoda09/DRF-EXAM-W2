from django.urls import path
from .views import *

urlpatterns = [
    path("", GroupListCreateView.as_view(), name="group-list-create"),
    path("<int:pk>/", GroupDetailView.as_view(), name="group-detail"),
    path("<int:group_id>/members/", GroupMemberListView.as_view(), name="group-members"),
    path("<int:group_id>/join/", JoinGroupView.as_view(), name="group-join"),
    path("<int:group_id>/leave/", LeaveGroupView.as_view(), name="group-leave"),
    path("<int:group_id>/messages/", GroupMessageListCreateView.as_view(), name="group-messages"),
]