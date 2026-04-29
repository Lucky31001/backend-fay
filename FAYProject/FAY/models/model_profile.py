import uuid

from django.contrib.auth.models import User
from django.db import models
from FAY.models.model_event_type import EventType


class Profile(models.Model):
    ROLE_CHOICES = (
        ("USER", "USER"),
        ("CREATOR", "CREATOR"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    description = models.TextField(blank=True, default="")
    image = models.ImageField(upload_to="profile/images/", blank=True, null=True)
    event_types = models.ManyToManyField(
        EventType, related_name="profile_events_type", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
