from .authentication import authentication_controller, logout_controller
from .index import index_controller
from .profile import (
    add_follow_controller,
    edit_field_profile_controller,
    profile_edit_controller,
    profile_followers_controller,
    profile_following_controller,
    profile_users_controller,
    remove_follow_controller,
)
from .registration import registrations_controller

__all__ = [
    "index_controller",
    "registrations_controller",
    "authentication_controller",
    "logout_controller",
    "profile_controller",
    "profile_users_controller",
    "profile_following_controller",
    "profile_followers_controller",
    "profile_edit_controller",
    "edit_field_profile_controller",
    "add_follow_controller",
    "remove_follow_controller",
]
