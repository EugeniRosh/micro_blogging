from core.presentation.views import index_controller
from django.urls import path

urlpatterns = [
    path("", index_controller, name="index"),
]
