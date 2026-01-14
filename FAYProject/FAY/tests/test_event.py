from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class EventTest(APITestCase):

    def setUp(self):
        self.creator = User.objects.create_user(
            username="creatoruser",
            email="test@test.test",
            password="password123"
        )
        self.creator.profile.role = "CREATOR"
        self.creator.profile.save()

    def test_create_event(self):
        data = {
            "name" : "soirée déguisées no limit",
            "location" : "Paris",
            "date" : 12/09/2022,
            "price" : 35,
            "creator": User,
            "link" : "https://fr.wikipedia.org/wiki/Moussa_Sanogo_(homme_politique)",
            "description": "Un super event",
            "type" : "Jazz",
            "note": 5.0,
            "capacity": 120,
        }

        response = self.client.post(
            "/api/event",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data.event_name, data.name)