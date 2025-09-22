from django.urls import path
from .views import UserProfileView

urlpatterns = [
    path("users/", UserProfileView.as_view(), name="user-profile-list"),
]
