from core.presentation.validators import ValidationAge   

from django import forms


class RegistrationsForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'size': 45}))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'size': 50}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'size': 46}))
    date_of_birth = forms.DateTimeField(
    label="Date of birth",
    
    input_formats=["%d.%m.%Y"],
    validators=[ValidationAge(min_age=18)],
    widget=forms.DateTimeInput(attrs={'placeholder': '01.01.0001','size':43 }) 
)
    def __init__(self, *args, **kwargs):
        super(RegistrationsForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter your password'})
        self.fields['date_of_birth'].widget.attrs.update({'placeholder': 'Enter your date of birth: 01.01.2000'}) 

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError("This field is required")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("This field is required")
        return email
    def true_emaile(self,email ):
        if "@" not in email:
            raise ValueError("Email must contain @ symbol")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("This field is required")
        return password

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if not date_of_birth:
            raise forms.ValidationError("This field is required")
        return date_of_birth

    def clean(self):
        cleaned_data = super(RegistrationsForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
