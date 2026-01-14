from FAY.models.model_event import Event
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class EventView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "GET reçu"})

    def post(self, request):
        name = request.data.get("name")
        location = request.data.get("location")
        price = request.data.get("price")
        link = request.data.get("link")
        description = request.data.get("description")
        event_type = request.data.get("event_type")
        note = request.data.get("note")
        capacity = request.data.get("capacity")

        if not name or not location:
            return Response(
                {"error": "Le nom et le lieu sont obligatoires"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        event = Event.objects.create(
            name=name,
            location=location,
            price=price or 0,
            link=link or "",
            description=description or "",
            event_type=event_type,
            note=note or 0,
            capacity=capacity or 0,
            creator=request.user,
        )

        return Response(
            {"message": "Event créé", "event_id": event.id, "event_name": event.name},
            status=status.HTTP_201_CREATED,
        )
