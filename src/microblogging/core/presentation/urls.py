from core.presentation.views import (
    add_twits_controller,
    authentication_controller,
    create_answer_to_twit_controller,
    delete_twits_controller,
    deleting_a_twit_likes_controller,
    edit_field_profile_controller,
    edit_twit_controller,
    follow_profile_controller,
    follower_profile_removal_controller,
    index_controller,
    like_twits_controller,
    logout_controller,
    profile_edit_controller,
    profile_followers_controller,
    profile_following_controller,
    profile_users_controller,
    registration_confirmations_controller,
    registrations_controller,
    repost_twits_controller,
    twit_repost_deletion_controller,
    view_twits_controller,
)
from django.urls import include, path

profile_patterns = [
    path("edit/", profile_edit_controller, name="edit_profile"),
    path("edit/<field>", edit_field_profile_controller, name="edit_field_profile"),
    path("<username>/", profile_users_controller, name="profile_users"),
    path("<username>/add_follow/", follow_profile_controller, name="add_follow"),
    path(
        "<username>/remove_follow/",
        follower_profile_removal_controller,
        name="remove_follow",
    ),
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
    path("edit/<int:twit_id>/", edit_twit_controller, name="edit_twit"),
    path("view/<int:twit_id>/", view_twits_controller, name="view_twit"),
    path("delete/<int:twit_id>/", delete_twits_controller, name="delete_twit"),
    path("add_like/<int:twit_id>/", like_twits_controller, name="add_like_twits"),
    path(
        "remove_like/<int:twit_id>/",
        deleting_a_twit_likes_controller,
        name="remove_like_twits",
    ),
    path("add_repost/<int:twit_id>/", repost_twits_controller, name="add_repost_twits"),
    path(
        "remove_repost/<int:twit_id>/",
        twit_repost_deletion_controller,
        name="remove_repost_twits",
    ),
]

urlpatterns = [
    path("", index_controller, name="index"),
    path("signup/", registrations_controller, name="registration"),
    path(
        "confirm_signup/", registration_confirmations_controller, name="confirm_signup"
    ),
    path("authentication/", authentication_controller, name="authentication"),
    path("logout/", logout_controller, name="logout"),
    path("profile/", include(profile_patterns)),
    path("twit/", include(twit_patterns)),
]
