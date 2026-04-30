from FAY.models.model_event_type import EventType
from FAY.models.model_profile import Profile
from FAY.service.service_event_type import extract_event_type_names
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


def _serialize_profile(profile, request=None):
    types = [et.name for et in profile.event_types.all()]
    image_url = (
        request.build_absolute_uri(profile.image.url)
        if profile.image and request
        else (profile.image.url if profile.image else None)
    )

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

    def get(self, request, pk=None):
        try:
            if pk:
                # Récupérer le profil d'un utilisateur spécifique par ID
                profile = Profile.objects.prefetch_related("event_types").get(id=pk)
            else:
                # Récupérer le profil de l'utilisateur actuellement authentifié
                profile = Profile.objects.prefetch_related("event_types").get(
                    user=request.user
                )
            return Response(
                _serialize_profile(profile, request), status=status.HTTP_200_OK
            )
        except Profile.DoesNotExist:
            return Response(
                {"error": "Profil non trouvé"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request):
        data = request.data
        print("Received data:", data)
        event_type_raw = (
            data.getlist("event_type")
            if hasattr(data, "getlist")
            else data.get("event_type")
        )
        event_type_names = extract_event_type_names(event_type_raw)

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


class ProfileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = (
            Profile.objects.prefetch_related("event_types")
            .filter(role="CREATOR")
            .exclude(user=request.user)
            .order_by("-created_at")
        )
        serialized_profiles = [
            _serialize_profile(profile, request) for profile in profiles
        ]
        return Response(serialized_profiles, status=status.HTTP_200_OK)
