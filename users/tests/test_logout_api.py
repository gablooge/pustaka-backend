from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from users.models import User


class LogoutTestCase(TestCase):
    def setUp(self):
        self.librarian = User.objects.create_superuser(
            username="test_superuser",
            email="test_superuser@test.com",
            password=settings.TEST_PASSWORD,
        )
        self.librarian.save()

        login_response = self.client.post(
            reverse("users_api:token_login"),
            data={"username": self.librarian.email, "password": settings.TEST_PASSWORD},
            content_type="application/json",
        )
        self.librarian_token = login_response.json()

    def test_logout_user_valid(self):
        uri = reverse("users_api:auth_logout")
        self.client.defaults["HTTP_AUTHORIZATION"] = f'Bearer {self.librarian_token.get("access")}'

        resp = self.client.post(
            uri,
            data={"refresh_token": self.librarian_token.get("refresh")},
            content_type="application/json",
        )
        assert resp.json()["message"] == "Logout successfully."
        assert resp.json()["success"] is True
        assert resp.status_code == 200

    def test_logout_user_invalid(self):
        uri = reverse("users_api:auth_logout")
        self.client.defaults["HTTP_AUTHORIZATION"] = f'Bearer {self.librarian_token.get("access")}'

        resp = self.client.post(
            uri,
            data={"refresh_token": "wrong"},
            content_type="application/json",
        )
        assert resp.json()["message"] == "Refresh Token not valid"
        assert resp.json()["success"] is False
        assert resp.status_code == 400

    def test_logout_401(self):
        uri = reverse("users_api:auth_logout")
        resp = self.client.post(uri, data={}, content_type="application/json")

        assert resp.json()["detail"] == "Authentication credentials were not provided."
        assert resp.status_code == 401
