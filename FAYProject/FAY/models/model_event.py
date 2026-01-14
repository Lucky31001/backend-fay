import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Event(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="events"
    )

    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    price = models.FloatField( default=0.0, validators=[
        MinValueValidator(0.0)
    ])
    link = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    event_type = models.CharField(max_length=255)
    note = models.FloatField( default=0.0, validators=[
        MinValueValidator(0.0),
        MaxValueValidator(5.0)
    ])
    capacity = models.IntegerField(default=0, validators=[
        MinValueValidator(0)
    ])

    def __str__(self):
        return self.name

