from django.urls import path
from .views import *

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", PhoneTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("me/", MeView.as_view(), name="me"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("profiles/", ProfileListView.as_view(), name="profile-list"),
    path("profiles/me/", MyProfileView.as_view(), name="my-profile"),
    path("profiles/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
    path("avatars/", AvatarCreateView.as_view(), name="avatar-create"),
    path("avatars/<int:pk>/", AvatarDetailView.as_view(), name="avatar-detail"),
]
