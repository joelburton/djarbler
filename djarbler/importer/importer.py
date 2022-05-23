"""Seed database with sample data from CSV Files."""

from csv import DictReader

from users.models import User
from warbles.models import Message

with open('users.csv') as users:
    User.objects.filter().delete()
    User.objects.bulk_create(User(**u) for u in DictReader(users))

with open('messages.csv') as messages:
    Message.objects.filter().delete()
    Message.objects.bulk_create(Message(**m) for m in DictReader(messages))

with open('follows.csv') as follows:
    Follow = User.following.through
    Follow.objects.filter().delete()
    Follow.objects.bulk_create(Follow(**f) for f in DictReader(follows))
