import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from FAY.models.model_event import Event
from FAY.models.model_event_type import EventType
from FAY.models.model_profile import Profile
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

TEST_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class EventTest(APITestCase):

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.user = User.objects.create_user(
            username="creatoruser", email="test@test.test", password="password123"
        )
        profile = Profile.objects.get(user=self.user)
        profile.role = "CREATOR"
        profile.save()

        self.refresh = RefreshToken.for_user(self.user)

    def test_create_event(self):
        expected_event_types = ["Jazz", "Electro"]
        data = {
            "name": "soirée déguisées no limit",
            "location": "Paris",
            "price": 35,
            "link": "https://fr.wikipedia.org/wiki/Moussa_Sanogo_(homme_politique)",
            "description": "Un super event",
            "event_type": expected_event_types,
            "date": "2025-12-31T23:59:00Z",
            "note": 5.0,
            "capacity": 120,
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}"
        )

        response = self.client.post("/api/event/", data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])
        self.assertCountEqual(response.data["event_type"], expected_event_types)

        # Vérifie que le creator est bien l'utilisateur connecté
        event = Event.objects.get(id=response.data["event_id"])
        self.assertEqual(event.creator, self.user)
        self.assertEqual(
            list(event.event_types.order_by("name").values_list("name", flat=True)),
            sorted(expected_event_types),
        )

    def test_create_event_with_custom_date(self):
        event_date = "2026-05-10T19:30:00Z"
        data = {
            "name": "event dated",
            "location": "Paris",
            "event_type": ["Jazz"],
            "date": event_date,
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}"
        )

        response = self.client.post("/api/event/", data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["date"].startswith("2026-05-10T19:30:00"))

        event = Event.objects.get(id=response.data["event_id"])
        expected = parse_datetime(event_date)
        if expected is not None and timezone.is_naive(expected):
            expected = timezone.make_aware(expected, timezone.get_current_timezone())
        self.assertEqual(event.date, expected)

    def test_create_event_with_single_event_type_value(self):
        data = {
            "name": "soirée simple",
            "location": "Paris",
            "price": 10,
            "link": "",
            "description": "",
            "event_type": "Fête",
            "date": "2026-05-22T20:00:00Z",
            "note": 4,
            "capacity": 60,
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}"
        )

        response = self.client.post("/api/event/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["event_type"], ["Fête"])

        event = Event.objects.get(id=response.data["event_id"])
        self.assertEqual(
            list(event.event_types.values_list("name", flat=True)), ["Fête"]
        )

    def test_get_events_returns_all_types(self):
        event = Event.objects.create(
            creator=self.user,
            name="soirée multi-types",
            location="Paris",
            price=0,
            link="",
            description="",
            note=0,
            capacity=0,
            date="2025-12-31T23:59:00Z",
        )
        jazz = EventType.objects.get_or_create(name="Jazz")[0]
        electro = EventType.objects.get_or_create(name="Electro")[0]
        event.event_types.set([jazz, electro])

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}"
        )

        response = self.client.get("/api/event/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            any(
                item["name"] == "soirée multi-types"
                and item["event_type"] == ["Jazz", "Electro"]
                for item in response.data
            )
        )

    def test_get_event_types_endpoint(self):
        EventType.objects.get_or_create(name="Electro")
        EventType.objects.get_or_create(name="Jazz")

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}"
        )

        response = self.client.get("/api/event-types/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["name"] for item in response.data], ["Electro", "Jazz"])
        self.assertTrue(all("id" in item for item in response.data))

    def test_create_event_with_image_upload(self):
        image = SimpleUploadedFile(
            "event.jpg", b"fake-image-content", content_type="image/jpeg"
        )
        data = {
            "name": "event image",
            "location": "Lyon",
            "event_type": "Jazz",
            "date": "2025-11-20T20:00:00Z",
            "image": image,
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}"
        )

        response = self.client.post("/api/event/", data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("/media/events/images/", response.data["image"])

        event = Event.objects.get(id=response.data["event_id"])
        self.assertTrue(event.image.name.startswith("events/images/"))
