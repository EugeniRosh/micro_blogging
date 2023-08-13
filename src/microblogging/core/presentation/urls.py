from core.presentation.views import (
    index_controller,
    profile_controller,
    registrations_controller,
)
from django.urls import include, path

profile_patterns = [
    path("", profile_controller, name="profile"),
]


urlpatterns = [
    path("", index_controller, name="index"),
    path("signup/", registrations_controller, name="registration"),
    path("profile/<username>/", include(profile_patterns)),
]
