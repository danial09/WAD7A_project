from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget =forms.PasswordInput())

    # An inline class to provide additional information about model and fields associated to the form.
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)