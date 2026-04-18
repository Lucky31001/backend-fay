from django.contrib.auth.models import User
from FAY.models.model_profile import Profile
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class AuthTest(APITestCase):

    def setUp(self):
        self.username = "testuser"
        self.email = "test@test.test"
        self.password = "password123"

    def _assert_access_token_role(self, access_token, expected_role):
        self.assertEqual(AccessToken(access_token)["role"], expected_role)

    def test_register_user(self):
        data = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": "CREATOR",
        }

        response = self.client.post("/api/register/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["refresh_token"])
        self.assertIsNotNone(response.data["access_token"])
        self._assert_access_token_role(response.data["access_token"], "CREATOR")

    def test_register_user_rejects_invalid_role(self):
        data = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": "ADMIN",
        }

        response = self.client.post("/api/register/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Role invalide")

    def test_login_user(self):

        User.objects.create_user(
            username=self.username, email=self.email, password=self.password
        )

        data = {"username": self.username, "password": self.password}

        response = self.client.post("/api/login/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["refresh_token"])
        self.assertIsNotNone(response.data["access_token"])
        self._assert_access_token_role(response.data["access_token"], "USER")

    def test_refresh_keeps_role_in_access_token(self):
        user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
        )
        Profile.objects.filter(user=user).update(role="CREATOR")

        login_response = self.client.post(
            "/api/login/",
            {"username": self.username, "password": self.password},
            format="json",
        )
        refresh_token = login_response.data["refresh_token"]

        refresh_response = self.client.post(
            "/api/token/refresh/",
            {"refresh": refresh_token},
            format="json",
        )

        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self._assert_access_token_role(refresh_response.data["access"], "CREATOR")
