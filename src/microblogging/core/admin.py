from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.dto import NotificationsAdminDTO
from core.business_logic.services import convert_data_from_form_in_dacite
from django import forms
from django.contrib import admin

from .models import Profiles, Twits, TwitsProfilesNotifications

# Register your models here.

if TYPE_CHECKING:
    from django.core.handlers.wsgi import WSGIRequest


class NotificationAdminForm(forms.ModelForm):
    users = forms.CharField(widget=forms.Textarea, required=False, strip=True)
    text = forms.CharField(
        label="Text", max_length=400, widget=forms.Textarea, strip=True
    )


class TwitsProfilesNotificationsAdmin(admin.ModelAdmin):
    form = NotificationAdminForm
    exclude = ["profile", "twit"]

    def save_model(
        self,
        request: WSGIRequest,
        obj: TwitsProfilesNotifications,
        form: NotificationAdminForm,
        change: bool,
    ) -> None:
        print("obj", type(obj))
        print("request", type(request))
        print("change", type(change))
        if form.is_valid():
            data = convert_data_from_form_in_dacite(
                dto=NotificationsAdminDTO, data=form.cleaned_data
            )

            if data.users:
                users = data.users.split("\r\n")
                users_from_db = Profiles.objects.filter(username__in=users)
            else:
                users_from_db = Profiles.objects.all()

            for user in users_from_db:
                user.notification.add(
                    Twits.objects.create(text=data.text, profile=request.user)
                )


admin.site.register(TwitsProfilesNotifications, TwitsProfilesNotificationsAdmin)
