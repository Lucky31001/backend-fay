from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class AuthTest(APITestCase):

    def setUp(self):
        self.username = "testuser"
        self.email = "test@test.test"
        self.password = "password123"

    def test_register_user(self):
        data = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
        }

        response = self.client.post("/api/register/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["refresh_token"])
        self.assertIsNotNone(response.data["access_token"])

    def test_login_user(self):

        User.objects.create_user(
            username=self.username, email=self.email, password=self.password
        )

        data = {"username": self.username, "password": self.password}

        response = self.client.post("/api/login/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["refresh_token"])
        self.assertIsNotNone(response.data["access_token"])
