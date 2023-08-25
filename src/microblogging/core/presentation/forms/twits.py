from core.presentation.validators import ValdateMaxValue
from django import forms


class TwitsForm(forms.Form):
    text = forms.CharField(
        label="Text", max_length=400, widget=forms.Textarea, strip=True
    )
    tag = forms.CharField(
        label="Tags",
        widget=forms.Textarea,
        strip=True,
        validators=[ValdateMaxValue(max_count=20)],
    )
