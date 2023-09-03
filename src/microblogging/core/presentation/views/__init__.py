from .authentication import authentication_controller, logout_controller
from .index import index_controller
from .profile import (
    edit_field_profile_controller,
    follow_profile_controller,
    profile_edit_controller,
    profile_followers_controller,
    profile_following_controller,
    profile_users_controller,
)
from .registration import (
    registration_confirmations_controller,
    registrations_controller,
)
from .twits import (
    add_twits_controller,
    create_answer_to_twit_controller,
    delete_twits_controller,
    edit_twit_controller,
    view_twits_controller,
)
from .twits_likes import like_twits_controller
from .twits_repost import repost_twits_controller

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
    "follow_profile_controller",
    "add_twits_controller",
    "view_twits_controller",
    "delete_twits_controller",
    "like_twits_controller",
    "repost_twits_controller",
    "create_answer_to_twit_controller",
    "edit_twit_controller",
    "registration_confirmations_controller",
]
