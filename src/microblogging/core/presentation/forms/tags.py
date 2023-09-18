from django import forms


class TagsSearchForm(forms.Form):
    tag = forms.CharField(label="tag", max_length=20, strip=True)
