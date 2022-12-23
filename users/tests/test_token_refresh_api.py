from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from users.models import User


class RefreshTokenTestCase(TestCase):
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

    def test_refresh_api_valid(self):
        uri = reverse("users_api:token_refresh")

        resp = self.client.post(
            uri,
            data={"refresh": self.librarian_token["refresh"]},
            content_type="application/json",
        )
        assert resp.json()["access"] is not None
        assert resp.status_code == 200

    def test_refresh_api_wrong_refresh(self):
        uri = reverse("users_api:token_refresh")

        resp = self.client.post(
            uri,
            data={"refresh": "wrong"},
            content_type="application/json",
        )
        assert resp.json()["detail"] == "Token is invalid or expired"
        assert resp.status_code == 401

    def test_refresh_api_invalid_refresh(self):
        uri = reverse("users_api:token_refresh")

        resp = self.client.post(
            uri,
            data={"refresh": None},
            content_type="application/json",
        )
        assert resp.json()["refresh"][0] == "This field may not be null."
        assert resp.status_code == 400

        resp = self.client.post(
            uri,
            data={"refresh": ""},
            content_type="application/json",
        )
        assert resp.json()["refresh"][0] == "This field may not be blank."
        assert resp.status_code == 400
