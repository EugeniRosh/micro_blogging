from core.presentation.views import (
    add_twits_controller,
    create_answer_to_twit_controller,
    delete_twits_controller,
    edit_field_profile_controller,
    follow_profile_controller,
    index_controller,
    like_twits_controller,
    profile_edit_controller,
    profile_followers_controller,
    profile_following_controller,
    profile_users_controller,
    registrations_controller,
    repost_twits_controller,
    view_twits_controller,
)
from django.urls import include, path

profile_patterns = [
    path("edit/", profile_edit_controller, name="edit_profile"),
    path("edit/<field>", edit_field_profile_controller, name="edit_field_profile"),
    path("<username>/", profile_users_controller, name="profile_users"),
    path("<username>/add_follow/", follow_profile_controller, name="follow"),
    path("<username>/followers/", profile_followers_controller, name="followers"),
    path("<username>/following/", profile_following_controller, name="following"),
]

twit_patterns = [
    path("add/", add_twits_controller, name="add_twit"),
    path(
        "add/<int:twit_id>/",
        create_answer_to_twit_controller,
        name="create_answer_to_twit",
    ),
    path("view/<int:twit_id>/", view_twits_controller, name="view_twit"),
    path("delete/<int:twit_id>/", delete_twits_controller, name="delete_twit"),
    path("like/<int:twit_id>/", like_twits_controller, name="like_twits"),
    path("repost/<int:twit_id>/", repost_twits_controller, name="repost_twits"),
]

urlpatterns = [
    path("", index_controller, name="index"),
    path("signup/", registrations_controller, name="registration"),
    path("profile/", include(profile_patterns)),
    path("twit/", include(twit_patterns)),
]
