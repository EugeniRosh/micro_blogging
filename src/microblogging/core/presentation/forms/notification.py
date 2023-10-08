from django import forms


class NotificationForm(forms.Form):
    text = forms.CharField(
        label="Text", max_length=400, widget=forms.Textarea, strip=True
    )
