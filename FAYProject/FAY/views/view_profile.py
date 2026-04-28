import profile

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from FAY.models.model_event_type import EventType
from FAY.models.model_profile import Profile
from FAY.service.service_event_type import extract_event_type_names

def _serialize_profile(profile, request=None):
    types = [et.name for et in profile.event_types.all()]
    image_url = request.build_absolute_uri(profile.image.url) if profile.image and request else (profile.image.url if profile.image else None)

    return {
        "id": profile.id,
        "name": profile.name,
        "description": profile.description,
        "image": image_url,
        "event_type": types,
    }

def _attach_event_types(profile, names):
    profile.event_types.set([EventType.objects.get_or_create(name=n)[0] for n in names])

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.prefetch_related("event_types")
        return Response([_serialize_event(e, request) for e in events])

    def post(self, request):
        data = request.data
        event_type_names = extract_event_type_names(
            data.getlist("event_type")
        )

        if not data.get("name"):
            return Response(
                {"error": "Le nom est obligatoires"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile = Profile.objects.get(user=request.user)
        profile.name = data.get("name")
        profile.description = data.get("description")
        profile.image = request.FILES.get("image")
        _attach_event_types(profile, event_type_names)
        profile.save()
        return Response(_serialize_profile(profile), status=status.HTTP_201_CREATED)

