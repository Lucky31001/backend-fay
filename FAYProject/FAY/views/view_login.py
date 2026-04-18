from django.contrib.auth import authenticate
from FAY.jwt_tokens import build_tokens_for_user
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            return Response(build_tokens_for_user(user))
        return Response(
            {"error": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED
        )
