from django.contrib.auth.models import User
from FAY.models.model_event import Event
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class EventTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="creatoruser", email="test@test.test", password="password123"
        )
        self.user.profile.role = "CREATOR"
        self.user.profile.save()

        self.refresh = RefreshToken.for_user(self.user)

    def test_create_event(self):
        data = {
            "name": "soirée déguisées no limit",
            "location": "Paris",
            "price": 35,
            "link": "https://fr.wikipedia.org/wiki/Moussa_Sanogo_(homme_politique)",
            "description": "Un super event",
            "event_type": "Jazz",
            "note": 5.0,
            "capacity": 120,
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}"
        )

        response = self.client.post("/api/event/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["event_name"], data["name"])

        # Vérifie que le creator est bien l'utilisateur connecté
        event = Event.objects.get(id=response.data["event_id"])
        self.assertEqual(event.creator, self.user)
