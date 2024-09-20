# userAuth_profile/forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    otp_verify = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Otp'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password','otp_verify']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        otp_verify = cleaned_data.get("otp_verify")
        
       
        
        return cleaned_data
