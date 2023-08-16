from core.presentation.views import (
    index_controller,
    profile_controller,
    profile_followers_controller,
    profile_following_controller,
    registrations_controller,
)
from django.urls import include, path

profile_patterns = [
    path("", profile_controller, name="profile"),
    path("followers/", profile_followers_controller, name="followers"),
    path("following/", profile_following_controller, name="following"),
]


urlpatterns = [
    path("", index_controller, name="index"),
    path("signup/", registrations_controller, name="registration"),
    path("profile/<username>/", include(profile_patterns)),
]
