from datetime import datetime

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from FAY.models.model_event import Event
from FAY.models.model_event_type import EventType
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


def _normalize_event_type_names(raw_event_types):
    if not raw_event_types:
        return []

    if isinstance(raw_event_types, str):
        candidates = raw_event_types.split(",")
    elif isinstance(raw_event_types, (list, tuple)):
        candidates = raw_event_types
    else:
        candidates = [raw_event_types]

    names = []
    for candidate in candidates:
        if isinstance(candidate, dict):
            candidate = candidate.get("name", "")
        name = str(candidate).strip()
        if name:
            names.append(name)

    return list(dict.fromkeys(names))


def _get_event_types(request):
    raw_event_types = request.data.get("event_types") or request.data.get("event_type")
    return _normalize_event_type_names(raw_event_types)


def _attach_event_types(event, event_type_names):
    event_types = [
        EventType.objects.get_or_create(name=name)[0] for name in event_type_names
    ]
    event.event_types.set(event_types)


def _serialize_event(event, request=None):
    event_types = [event_type.name for event_type in event.event_types.all()]
    image_url = None
    if event.image:
        image_url = event.image.url
        if request is not None:
            image_url = request.build_absolute_uri(image_url)

    return {
        "id": event.id,
        "name": event.name,
        "date": event.date.isoformat() if event.date else None,
        "location": event.location,
        "price": event.price,
        "link": event.link,
        "description": event.description,
        "image": image_url,
        "event_type": event_types[0] if event_types else None,
        "event_types": event_types,
        "note": event.note,
        "capacity": event.capacity,
    }


def _serialize_event_type(event_type):
    return {"id": event_type.id, "name": event_type.name}


class EventView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Event.objects.prefetch_related("event_types")
        return Response([_serialize_event(event, request) for event in events])

    def post(self, request):
        data = request.data
        event_type_names = _get_event_types(request)
        raw_date = data.get("date")

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

        event_date = None
        if raw_date:
            if isinstance(raw_date, datetime):
                event_date = raw_date
            else:
                event_date = parse_datetime(str(raw_date))

            if event_date is None:
                return Response(
                    {
                        "error": "Format de date invalide. Utilise le format ISO 8601 (ex: 2026-05-10T19:30:00Z)."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if timezone.is_naive(event_date):
                event_date = timezone.make_aware(
                    event_date, timezone.get_current_timezone()
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
            {
                "message": "Event créé",
                "event_id": event.id,
                **_serialize_event(event, request),
            },
            status=status.HTTP_201_CREATED,
        )


class EventTypeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        event_types = EventType.objects.order_by("name")
        return Response(
            [_serialize_event_type(event_type) for event_type in event_types]
        )
