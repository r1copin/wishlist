from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthTests(APITestCase):
    def setUp(self):
        self.register_url = "/api/register/"
        self.login_url = "/api/login/"
        self.me_url = "/api/me/"
        self.user_data = {
            "username": "tanya-kta",
            "email": "tanya-kta@ex.com",
            "password": "123123",
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, "tanya-kta")

    def test_login_user(self):
        User.objects.create_user(**self.user_data)
        login_payload = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, login_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_me_authenticated(self):
        user = User.objects.create_user(**self.user_data)
        access_token = str(RefreshToken.for_user(user).access_token)
        auth_header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

        response = self.client.get(self.me_url, **auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "tanya-kta")

    def test_me_unauthenticated(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
