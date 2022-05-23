from django.test import TestCase

from users.models import User
from .models import Message


class MessageModelTest(TestCase):
    def setUp(self):
        self.user = User.signup("testing", "testing@test.com", "password")
        self.msg = Message.objects.create(text="text", user=self.user)

    def test_message_model(self):
        self.assertEqual(self.user.messages.get().text, "text")

    def test_message_likes(self):
        # make a second message but don't like it
        Message(text="b", user_id=self.user)

        self.user.liked_messages.add(self.msg)

        self.assertEqual(self.user.liked_messages.count(), 1)
        self.assertTrue(self.user.liked_messages.contains(self.msg))
