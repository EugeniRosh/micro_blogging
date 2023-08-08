from core.presentation.views import index_controller, registrations_controller
from django.urls import path

urlpatterns = [
    path("", index_controller, name="index"),
    path("signup/", registrations_controller, name="registration"),
]
