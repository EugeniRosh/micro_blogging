from core.presentation.views import (
    add_follow_controller,
    add_twits_controller,
    edit_field_profile_controller,
    index_controller,
    profile_edit_controller,
    profile_followers_controller,
    profile_following_controller,
    profile_users_controller,
    registrations_controller,
    remove_follow_controller,
)
from django.urls import include, path

profile_patterns = [
    path("edit/", profile_edit_controller, name="edit_profile"),
    path("edit/<field>", edit_field_profile_controller, name="edit_field_profile"),
    path("<username>/", profile_users_controller, name="profile_users"),
    path("<username>/add_follow/", add_follow_controller, name="add_follow"),
    path("<username>/remove_follow/", remove_follow_controller, name="remove_follow"),
    path("<username>/followers/", profile_followers_controller, name="followers"),
    path("<username>/following/", profile_following_controller, name="following"),
]

twit_patterns = [
    path("add/", add_twits_controller, name="add_twit"),
]

urlpatterns = [
    path("", index_controller, name="index"),
    path("signup/", registrations_controller, name="registration"),
    path("profile/", include(profile_patterns)),
    path("twit/", include(twit_patterns)),
]
