from django.urls import path

from .views import (
    ChangePasswordView,
    UserProfileView,
    UserRegistrationView,
    current_user,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("me/", current_user, name="current-user"),
]
