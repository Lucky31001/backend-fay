from django.contrib.auth.models import User
from FAY.models.model_profile import Profile
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class ProfileTest(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(
            username="user1", email="user1@test.test", password="password123"
        )
        self.user_2 = User.objects.create_user(
            username="user2", email="user2@test.test", password="password123"
        )
        self.user_3 = User.objects.create_user(
            username="user3", email="user3@test.test", password="password123"
        )

        profile_1 = Profile.objects.get(user=self.user_1)
        profile_1.name = "Alice"
        profile_1.role = "CREATOR"
        profile_1.save()

        profile_2 = Profile.objects.get(user=self.user_2)
        profile_2.name = "Bob"
        profile_2.role = "USER"
        profile_2.save()

        profile_3 = Profile.objects.get(user=self.user_3)
        profile_3.name = "Charlie"
        profile_3.role = "CREATOR"
        profile_3.save()

        refresh = RefreshToken.for_user(self.user_1)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_update_profile(self):
        data = {
            "name": "Alice Updated",
            "description": "Nouvelle description",
            "event_type": ["Jazz", "Electro"],
        }

        response = self.client.post("/api/profile/", data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Alice Updated")

        profile = Profile.objects.get(user=self.user_1)
        self.assertEqual(profile.name, "Alice Updated")

    def test_get_authenticated_user_profile(self):
        # Retrieve profile of the authenticated user
        response = self.client.get("/api/profile/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Alice")

    def test_get_profiles_list(self):
        response = self.client.get("/api/profiles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Charlie")
