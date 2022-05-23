from django.db import models


class Message(models.Model):
    """An individual message ("warble")."""

    text = models.TextField(max_length=140)

    timestamp = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="messages",
    )
