from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models

DEFAULT_IMAGE = "/static/images/default-pic.png"
DEFAULT_HEADER_IMAGE = "/static/images/warbler-hero.jpg"


class User(AbstractUser):
    """User in the system."""

    # overriding default from AbstractUser to make required
    email = models.EmailField()

    image = models.ImageField(default=DEFAULT_IMAGE)

    header_image = models.ImageField(default=DEFAULT_HEADER_IMAGE)

    bio = models.TextField(blank=True)

    location = models.CharField(max_length=50, blank=True)

    # Normally, when Django makes a m2m to the same model, it assumes that this
    # is "symmetrical" (if A is friends with B, B is friends with A). However,
    # this is not how following works, so make this asymmetrical.
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
    )

    liked_messages = models.ManyToManyField(
        "warbles.Message",
        related_name="likers",
    )

    @classmethod
    def signup(cls, username, email, password, image=DEFAULT_IMAGE) -> User:
        """Signup a new user."""

        return User.objects.create_user(username, email, password, image=image)

    def is_followed_by(self, other_user):
        """Is this user followed by `other user`?"""

        return self.followers.contains(other_user)

    def is_following(self, other_user):
        """Is this user following `other_user`?"""

        return self.following.contains(other_user)
