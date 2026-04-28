from datetime import datetime

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from FAY.models.model_event import Event
from FAY.models.model_event_type import EventType
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from FAY.service.service_event_type import extract_event_type_names


def _parse_event_date(raw):
    """ S'assurer d'avoir un datetime aware à partir d'une string ou d'un datetime, ou None si c'est invalide """
    if not raw:
        return None
    dt = raw if isinstance(raw, datetime) else parse_datetime(str(raw))
    if dt is None:
        return None
    return dt if timezone.is_aware(dt) else timezone.make_aware(dt, timezone.get_current_timezone())


def _attach_event_types(event, names):
    event.event_types.set([EventType.objects.get_or_create(name=n)[0] for n in names])


def _serialize_event(event, request=None):
    types = [et.name for et in event.event_types.all()]
    image_url = request.build_absolute_uri(event.image.url) if event.image and request else (event.image.url if event.image else None)

    return {
        "id": event.id,
        "name": event.name,
        "date": event.date.isoformat() if event.date else None,
        "location": event.location,
        "price": event.price,
        "link": event.link,
        "description": event.description,
        "image": image_url,
        "event_type": types,
        "note": event.note,
        "capacity": event.capacity,
    }

def _serialize_event_type(et):
    return {"id": et.id, "name": et.name}


class EventView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Event.objects.prefetch_related("event_types")
        return Response([_serialize_event(e, request) for e in events])

    def post(self, request):
        data = request.data
        event_type_names = extract_event_type_names(
            data.getlist("event_type")
        )

        if not data.get("name") or not data.get("location"):
            return Response(
                {"error": "Le nom et le lieu sont obligatoires"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not event_type_names:
            return Response(
                {"error": "Au moins un type d'événement est obligatoire"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        event_date = _parse_event_date(data.get("date"))
        if event_date is None:
            return Response(
                {"error": "Format de date invalide. Utilise le format ISO 8601 (ex: 2026-05-10T19:30:00Z)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        event = Event.objects.create(
            name=data.get("name"),
            date=event_date or timezone.now(),
            location=data.get("location"),
            price=data.get("price") or 0,
            link=data.get("link") or "",
            description=data.get("description") or "",
            image=request.FILES.get("image"),
            note=data.get("note") or 0,
            capacity=data.get("capacity") or 0,
            creator=request.user,
        )
        _attach_event_types(event, event_type_names)

        return Response(
            {"message": "Event créé", "event_id": event.id, **_serialize_event(event, request)},
            status=status.HTTP_201_CREATED,
        )


class EventTypeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response([_serialize_event_type(et) for et in EventType.objects.order_by("name")])