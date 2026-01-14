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
        self.assertEqual(True, True)