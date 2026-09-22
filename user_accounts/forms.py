import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationForm(forms.Form):
    fullname = forms.CharField(
        max_length=100,
        required=True,
        error_messages={'required': 'Full Name is required.'}
    )
    email = forms.EmailField(
        required=True,
        error_messages={'required': 'Email address is required.', 'invalid': 'Enter a valid email address.'}
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        error_messages={'required': 'Phone number is required.'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=6,
        required=True,
        error_messages={
            'required': 'Password is required.',
            'min_length': 'Password must be at least 6 characters long.'
        }
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        error_messages={'required': 'Confirm password is required.'}
    )

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        cleaned_digits = re.sub(r'\D', '', phone)
        if len(cleaned_digits) < 10:
            raise ValidationError('Enter a valid 10-digit phone number.')
        return phone

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        if not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            raise ValidationError('Password must contain both letters and numbers.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.CharField(
        required=True,
        error_messages={'required': 'Email or Username is required.'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        error_messages={'required': 'Password is required.'}
    )
