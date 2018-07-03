from django import forms


class AuthenticateSessionForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
