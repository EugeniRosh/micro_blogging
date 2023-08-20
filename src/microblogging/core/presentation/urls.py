from core.presentation.views import (
    edit_field_profile_controller,
    index_controller,
    profile_controller,
    profile_edit_controller,
    profile_followers_controller,
    profile_following_controller,
    registrations_controller,
)
from django.urls import include, path

profile_patterns = [
    path("edit/", profile_edit_controller, name="edit_profile"),
    path("edit/<field>", edit_field_profile_controller, name="edit_field_profile"),
    path("<username>/", profile_controller, name="profile"),
    path("<username>/followers/", profile_followers_controller, name="followers"),
    path("<username>/following/", profile_following_controller, name="following"),
]


urlpatterns = [
    path("", index_controller, name="index"),
    path("signup/", registrations_controller, name="registration"),
    path("profile/", include(profile_patterns)),
]
