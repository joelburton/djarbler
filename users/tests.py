from bs4 import BeautifulSoup
from django.test import TestCase

from users.models import User
from warbles.models import Message


class UserModelTestCase(TestCase):
    """Add sample data."""

    def setUp(self):
        self.u1 = User.signup("test1", "email@email.com", "password")
        self.u2 = User.signup("test2", "email2@email.com", "password")

    def test_user_model(self):
        """Does basic model work?"""

        self.assertEqual(self.u1.messages.count(), 0)

    # ################################# following tests

    def test_user_follows(self):
        self.u1.following.add(self.u2)
        self.assertEqual(self.u2.following.count(), 0)
        self.assertEqual(self.u2.followers.count(), 1)
        self.assertEqual(self.u1.followers.count(), 0)
        self.assertEqual(self.u1.following.count(), 1)

        self.assertEqual(self.u2.followers.first(), self.u1)
        self.assertEqual(self.u1.following.first(), self.u2)

    def test_is_following(self):
        self.u1.following.add(self.u2)

        self.assertTrue(self.u1.is_following(self.u2))
        self.assertFalse(self.u2.is_following(self.u1))

    def test_is_followed_by(self):
        self.u1.following.add(self.u2)

        self.assertTrue(self.u2.is_followed_by(self.u1))
        self.assertFalse(self.u1.is_followed_by(self.u2))

    # ################################# signup tests

    def test_valid_signup(self):
        u_test = User.signup("testtesttest", "testtest@test.com", "password")

        self.assertEqual(u_test.username, "testtesttest")
        self.assertEqual(u_test.email, "testtest@test.com")
        self.assertNotEqual(u_test.password, "password")
        # Hashed strings should start with marker
        self.assertTrue(u_test.password.startswith('pbkdf2_sha256'))

    # ################################# auth tests

    def test_valid_authentication(self):
        self.assertTrue(
            self.client.login(username="test1", password="password"))

    def test_invalid_username(self):
        self.assertFalse(
            self.client.login(username="bad-username", password="password"))

    def test_wrong_password(self):
        self.assertFalse(
            self.client.login(username="test1", password="bad-password"))


class UserListViewTestCase(TestCase):
    def setUp(self):
        self.u1 = User.signup("u1", "u1@test.com", "pass")
        self.u2 = User.signup("u2", "u2@test.com", "pass")

    def test_auth(self):
        resp = self.client.get("/users/")
        self.assertRedirects(resp, "/accounts/login/?next=/users/")

    def test_list(self):
        self.client.force_login(self.u1)
        resp = self.client.get("/users/")
        self.assertContains(resp, "@u1")
        self.assertContains(resp, "@u2")

    def test_list_search(self):
        self.client.force_login(self.u1)
        resp = self.client.get("/users/?q=1")
        self.assertContains(resp, "@u1")
        self.assertNotContains(resp, "@u2")


class UserShowViewTestCase(TestCase):
    def setUp(self):
        self.u1 = User.signup("u1", "u1@test.com", "pass")

    def test_auth(self):
        resp = self.client.get(f"/users/{self.u1.id}/")
        self.assertRedirects(resp, "/accounts/login/?next=/users/1/")

    def test_user_show(self):
        self.client.force_login(self.u1)
        resp = self.client.get(f"/users/{self.u1.id}/")
        self.assertContains(resp, "@u1")


class UserLikesViewTestCase(TestCase):
    def setUp(self):
        self.u1 = User.signup("u1", "u1@test.com", "pass")
        self.u2 = User.signup("u2", "u2@test.com", "pass")
        self.m1 = Message.objects.create(text="m1-text", user=self.u1)
        self.m2 = Message.objects.create(text="m2-text", user=self.u1)
        self.u1.liked_messages.add(self.m1)

    def test_user_show_with_likes(self):
        self.client.force_login(self.u1)

        resp = self.client.get(f"/users/{self.u1.id}/")

        self.assertContains(resp, "@u1")

        soup = BeautifulSoup(resp.content, 'html.parser')
        found = soup.find_all("li", {"class": "stat"})
        self.assertEqual(len(found), 4)
        self.assertIn("2", found[0].text)  # 2 messages
        self.assertIn("0", found[1].text)  # 0 followers
        self.assertIn("0", found[2].text)  # 0 following
        self.assertIn("1", found[3].text)  # 1 like

    def test_add_like(self):
        self.client.force_login(self.u2)

        resp = self.client.post(f"/messages/{self.m1.id}/like/")
        self.assertRedirects(resp, "/")
        self.assertTrue(self.u2.liked_messages.contains(self.m1))

    def test_remove_like(self):
        self.client.force_login(self.u2)
        self.u2.liked_messages.add(self.m1)

        resp = self.client.post(f"/messages/{self.m1.id}/like/")
        self.assertRedirects(resp, "/")
        self.assertFalse(self.u2.liked_messages.contains(self.m1))

    def test_cant_self_obsess(self):
        self.client.force_login(self.u1)

        resp = self.client.post(f"/messages/{self.m1.id}/like/")
        self.assertEqual(resp.status_code, 403)
