# File path: C:\hosting\skillscontinua_hosting\accounts\forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Used for account recovery.")
    preferred_language = forms.ChoiceField(choices=User.LANGUAGE_CHOICES, initial="en")

    class Meta:
        model = User
        fields = ("username", "email", "preferred_language", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.preferred_language = self.cleaned_data["preferred_language"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Thin wrapper so we can style it with crispy later if needed."""
    username = forms.CharField(
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )