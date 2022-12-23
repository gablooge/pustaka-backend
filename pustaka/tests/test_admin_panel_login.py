import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

User = get_user_model()


@pytest.mark.django_db
class LoginTest(TestCase):
    def setUp(self):
        self.john_data = {
            "username": "john",
            "email": "jlennon@beatles.com",
            "password": "glass onion",
        }
        User.objects.create_user(
            username=self.john_data.get("username"),
            email=self.john_data.get("email"),
            password=self.john_data.get("password"),
        )

    def test_get_login_valid(self):
        # Issue a GET request.
        url = reverse("admin:login")
        response = self.client.get(url)

        self.assertTrue(response.context["user"].is_anonymous)
        self.assertEqual(response.status_code, 200)

    def test_post_login_valid_with_username(self):
        url = reverse("admin:login")

        login = self.client.login(
            username=self.john_data.get("username"),
            password=self.john_data.get("password"),
        )
        self.assertTrue(login)

        response = self.client.post(url, self.john_data)

        self.assertEqual(
            self.john_data.get("username"), response.context["user"].username
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_active)

    def test_post_login_valid_with_email(self):
        url = reverse("admin:login")

        login = self.client.login(
            username=self.john_data.get("email"),
            password=self.john_data.get("password"),
        )
        self.assertTrue(login)

        response = self.client.post(url, self.john_data)

        self.assertEqual(self.john_data.get("email"), response.context["user"].email)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_active)

    @parameterized.expand(
        [
            ["wrong", "wrong"],  # wrong username & password
            ["", ""],  # empty credentials
        ]
    )
    def test_post_login_invalid_credentials(self, username, password):
        url = reverse("admin:login")
        user = {"username": username, "password": password}
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_anonymous)
        self.assertFalse(response.context["user"].is_active)
