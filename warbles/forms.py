from django import forms

from warbles.models import Message


class MessageCreateForm(forms.ModelForm):
    """Create a message."""

    class Meta:
        model = Message
        fields = "text",
