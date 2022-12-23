from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from jwt import decode
from mixer.backend.django import mixer
from parameterized import parameterized

from users.models import User


class LoginTestCase(TestCase):
    def setUp(self):
        self.librarian = User.objects.create_superuser(
            username="test_superuser",
            email="test_superuser@test.com",
            password=settings.TEST_PASSWORD,
        )
        self.librarian.save()

        self.user = mixer.blend(User)
        self.user.set_password(settings.TEST_PASSWORD)
        self.user.is_staff = False
        self.user.is_superuser = False
        self.user.save()

    def test_login_superuser_valid_with_email(self):
        """Login with valid email"""
        uri = reverse("users_api:token_login")
        resp = self.client.post(
            uri,
            data={"username": self.librarian.email, "password": settings.TEST_PASSWORD},
            content_type="application/json",
        )

        assert (
            decode(resp.json()["access"], settings.SECRET_KEY, algorithms=["HS256"])[
                "user_id"
            ]
            == self.librarian.id
        )
        assert resp.status_code == 200

    def test_login_user_valid(self):
        uri = reverse("users_api:token_login")
        resp = self.client.post(
            uri,
            data={"username": self.user.username, "password": settings.TEST_PASSWORD},
            content_type="application/json",
        )

        assert (
            decode(resp.json()["access"], settings.SECRET_KEY, algorithms=["HS256"])[
                "user_id"
            ]
            == self.user.id
        )
        assert resp.status_code == 200

    def test_login_superuser_empty_payload(self):
        uri = reverse("users_api:token_login")
        resp = self.client.post(uri, data={}, content_type="application/json")

        assert resp.json()["username"][0] == "This field is required."
        assert resp.status_code == 400

    @parameterized.expand(
        [
            # blank password
            ["test_superuser", "", "password", "This field may not be blank."],
            # blank username
            [
                "",
                settings.TEST_PASSWORD,
                "username",
                "This field may not be blank.",
            ],
            # null password
            ["test_superuser", None, "password", "This field may not be null."],
            # null username
            [
                None,
                settings.TEST_PASSWORD,
                "username",
                "This field may not be null.",
            ],
        ]
    )
    def test_login_superuser_invalid_payload(self, username, password, field, error):
        uri = reverse("users_api:token_login")
        resp = self.client.post(
            uri,
            data={"username": username, "password": password},
            content_type="application/json",
        )

        assert resp.json()[field][0] == error
        assert resp.status_code == 400

    @parameterized.expand(
        [
            ("wrong", "wrong"),  # wrong username and password
            ("wrong", settings.TEST_PASSWORD),  # wrong password
        ],
    )
    def test_login_superuser_invalid(self, username, password):
        uri = reverse("users_api:token_login")
        resp = self.client.post(
            uri,
            data={"username": username, "password": password},
            content_type="application/json",
        )

        assert (
            resp.json()["detail"]
            == "No active account found with the given credentials"
        )
        assert resp.status_code == 401

    def test_login_get_not_allowed(self):
        uri = reverse("users_api:token_login")
        resp = self.client.get(uri, content_type="application/json")

        assert resp.json()["detail"] == 'Method "GET" not allowed.'
        assert resp.status_code == 405
