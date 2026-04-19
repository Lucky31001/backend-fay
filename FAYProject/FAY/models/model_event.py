import uuid

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from FAY.models.model_event_type import EventType


class Event(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")

    name = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=255)
    price = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    link = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to="events/images/", blank=True, null=True)
    event_types = models.ManyToManyField(
        EventType, related_name="events_type", blank=True
    )
    note = models.FloatField(
        default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    capacity = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name
