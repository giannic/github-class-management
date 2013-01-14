from django import forms
from registration.forms import RegistrationForm


class CustomRegistrationForm(RegistrationForm):
        first_name = forms.CharField()
        last_name = forms.CharField()
        github_username = forms.CharField()
