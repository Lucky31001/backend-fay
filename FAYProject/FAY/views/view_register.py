from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role", "USER")

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Utilisateur déjà existant"}, status=status.HTTP_409_CONFLICT
            )

        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        user.profile.role = role
        user.profile.save()

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh_token": str(refresh),
                "access_token": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
