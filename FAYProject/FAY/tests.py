from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class RegisterTest(APITestCase):

    def test_register_user(self):
        data = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "password123"
        }

        response = self.client.post(
            "/auth/user/register/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "testuser")

        user = User.objects.get(username="testuser")
        self.assertEqual(user.profile.role, "USER")
