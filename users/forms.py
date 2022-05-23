from django import forms
from django.core.exceptions import ValidationError

from users.models import User


class SignupForm(forms.ModelForm):
    """Form for adding users."""

    class Meta:
        model = User
        fields = "username", "email", "password", "image"
        widgets = {
            "password": forms.PasswordInput(),
        }


class ProfileForm(forms.ModelForm):
    """Form for editing users."""

    confirm = forms.CharField(
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = "username", "email", "image", "header_image", "bio"

    def clean_confirm(self):
        """Check that password-confirm field is correct."""

        if not self.instance.check_password(self.cleaned_data["confirm"]):
            raise ValidationError("Not correct password")
        return self.cleaned_data["confirm"]
