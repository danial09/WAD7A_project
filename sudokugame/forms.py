from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already being used")
        return email

    # An inline class to provide additional information about model and fields associated to the form.
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
