from django.contrib.auth.models import User
from FAY.jwt_tokens import build_tokens_for_user
from FAY.models.model_profile import Profile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class RegisterView(APIView):

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role", "USER")

        allowed_roles = {value for value, _label in Profile.ROLE_CHOICES}
        if role not in allowed_roles:
            return Response(
                {
                    "error": "Role invalide",
                    "allowed_roles": sorted(allowed_roles),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Utilisateur déjà existant"}, status=status.HTTP_409_CONFLICT
            )

        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        Profile.objects.filter(user=user).update(role=role)

        tokens = build_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_201_CREATED)
